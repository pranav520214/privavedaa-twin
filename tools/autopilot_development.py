"""Active, bounded local development queue. Produces proposals; never applies or executes them."""

import argparse
import json
import os
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.ollama_delegate import ROOT, delegate  # noqa: E402

STATE = ROOT / ".context/autopilot-status.json"
STOP = ROOT / ".context/autopilot.stop"
LOCK = ROOT / ".context/autopilot.lock"


class Job(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    id: str = Field(pattern=r"^[a-zA-Z0-9_]+$")
    role: Literal["coder", "reviewer", "test_writer", "documentation"]
    task_file: str


def load_queue(path: Path) -> list[Job]:
    jobs = [Job.model_validate(item) for item in json.loads(path.read_text(encoding="utf-8"))]
    if len({job.id for job in jobs}) != len(jobs):
        raise ValueError("Queue ids must be unique")
    for job in jobs:
        target = (ROOT / job.task_file).resolve()
        if not target.is_relative_to((ROOT / ".tasks").resolve()) or target.suffix != ".md":
            raise ValueError("Queue may contain only curated .tasks/*.md files")
    return jobs


def write_state(state: dict[str, object]) -> None:
    STATE.parent.mkdir(exist_ok=True)
    temporary = STATE.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, indent=2), encoding="utf-8")
    temporary.replace(STATE)


def run(queue: Path, watch: bool, max_tasks: int, idle_timeout: int) -> None:
    if not 1 <= max_tasks <= 100 or not 1 <= idle_timeout <= 43200:
        raise ValueError("Invalid worker bounds")
    # Exclusive creation prevents duplicate active workers. Never delete someone else's lock.
    LOCK.parent.mkdir(exist_ok=True)
    with LOCK.open("x", encoding="utf-8") as handle:
        handle.write(str(os.getpid()))
    outcomes: dict[str, str] = {}
    if STATE.exists():
        previous = json.loads(STATE.read_text(encoding="utf-8"))
        outcomes = previous.get("jobs", {})
    state: dict[str, object] = {
        "pid": os.getpid(),
        "mode": "local_proposals_only",
        "started_at": datetime.now(UTC).isoformat(),
        "jobs": outcomes,
        "status": "running",
    }
    attempts, last_work = 0, time.monotonic()
    try:
        while attempts < max_tasks and not STOP.exists():
            jobs = load_queue(queue)
            pending = [job for job in jobs if job.id not in outcomes]
            if not pending:
                state.update(status="idle", active_job=None)
                write_state(state)
                if not watch or time.monotonic() - last_work >= idle_timeout:
                    break
                time.sleep(2)
                continue
            job = pending[0]
            state.update(status="running", active_job=job.id)
            write_state(state)
            try:
                result = delegate(ROOT / job.task_file, job.role, timeout=900)
                outcomes[job.id] = "needs_orchestrator_review"
                state["last_result"] = str(result.relative_to(ROOT))
                print(f"{job.id}: proposal saved for review", flush=True)
            except Exception as error:
                outcomes[job.id] = f"failed: {type(error).__name__}"
                print(f"{job.id}: failed ({type(error).__name__}); no code applied", flush=True)
            attempts += 1
            last_work = time.monotonic()
        state.update(status="stopped", active_job=None, finished_at=datetime.now(UTC).isoformat())
        write_state(state)
    finally:
        LOCK.unlink(missing_ok=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, default=ROOT / ".tasks/queue.json")
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--max-tasks", type=int, default=12)
    parser.add_argument("--idle-timeout", type=int, default=1800)
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--stop", action="store_true")
    args = parser.parse_args()
    if args.status:
        print(STATE.read_text(encoding="utf-8") if STATE.exists() else "Worker has not started")
    elif args.stop:
        STOP.touch()
        print("Stop requested after current bounded request finishes")
    else:
        if STOP.exists():
            STOP.unlink()
        run(args.queue, args.watch, args.max_tasks, args.idle_timeout)
