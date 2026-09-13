"""Submit explicitly scoped synthetic/code context; save proposals, never apply them."""

import argparse
import hashlib
import json
import sys
from pathlib import Path
from urllib.request import ProxyHandler, Request, build_opener

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.agent_protocol import AgentResponse  # noqa: E402
from tools.model_router import choose_model, installed_models, local_url  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def delegate(task_file: Path, role: str, timeout: int = 300) -> Path:
    config = yaml.safe_load((ROOT / "configs/ollama.yaml").read_text())
    base = local_url(config["ollama"]["base_url"])
    task = task_file.read_text(encoding="utf-8")
    # Explicit metadata limits scope; it is not an automated PHI detector.
    meta = json.loads(task.splitlines()[0])
    if meta["context_type"] != "synthetic_or_code" or len(task) > 60000:
        raise ValueError("Only curated code/synthetic tasks up to 60 KB are allowed")
    task_id = meta["task_id"]
    if not isinstance(task_id, str) or not task_id.replace("_", "").isalnum():
        raise ValueError("Invalid task id")
    model = choose_model(installed_models(base), config["local_agents"][role])
    template = (ROOT / "prompts" / f"{role}.md").read_text(encoding="utf-8")
    payload = {
        "model": model,
        "stream": False,
        "think": False,
        "format": AgentResponse.model_json_schema(),
        "messages": [{"role": "system", "content": template}, {"role": "user", "content": task}],
        "options": {
            "temperature": 0,
            "seed": 42,
            "num_ctx": 8192,
            "num_predict": 4500 if role == "coder" else 1600,
        },
    }
    request = Request(
        base + "/api/chat",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    opener = build_opener(ProxyHandler({}))
    with opener.open(request, timeout=timeout) as response:
        body = json.load(response)
    proposal = AgentResponse.model_validate_json(body["message"]["content"])
    proposal.check_scope(task_id, set(meta["allowed_files"]))
    target = ROOT / ".tasks" / "results" / f"{task_id}_{role}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(proposal.model_dump_json(indent=2), encoding="utf-8")
    target.with_suffix(".audit.json").write_text(
        json.dumps(
            {
                "model": model,
                "task_sha256": hashlib.sha256(task.encode()).hexdigest(),
                "response_model": body.get("model"),
                "status": "proposal_only_not_approved",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return target


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--role", choices=["coder", "reviewer", "test_writer", "documentation"], required=True
    )
    parser.add_argument("--task-file", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()
    print(delegate(args.task_file, args.role, args.timeout))
