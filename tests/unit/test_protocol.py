import pytest
from pydantic import ValidationError

from tools.agent_protocol import AgentResponse, FileProposal
from tools.model_router import choose_model, local_url


def test_scope_and_malformed():
    with pytest.raises(ValidationError):
        AgentResponse.model_validate_json('{"task_id":"x"}')
    for path in ["../secret", "C:/secret", "/root", "a\\b"]:
        with pytest.raises(ValidationError):
            FileProposal(path=path, content="x")
    proposal = AgentResponse(
        task_id="x",
        status="needs_review",
        summary="x",
        files_to_create=[FileProposal(path="a.py", content="")],
        files_to_modify=[],
        patch="",
        tests_proposed=[],
        assumptions=[],
        risks=[],
        questions=[],
    )
    with pytest.raises(ValueError):
        proposal.check_scope("x", {"b.py"})
    with pytest.raises(ValueError):
        proposal.check_scope("y", {"a.py"})
    proposal.check_scope("x", {"a.py"})


def test_local_routing():
    assert choose_model(["qwen2.5-coder:3b"]) == "qwen2.5-coder:3b"
    with pytest.raises(RuntimeError):
        choose_model(["medgemma:4b"])
    for url in [
        "https://example.com",
        "http://example.com",
        "http://localhost@evil.test",
        "http://localhost/v1",
    ]:
        with pytest.raises(ValueError):
            local_url(url)
