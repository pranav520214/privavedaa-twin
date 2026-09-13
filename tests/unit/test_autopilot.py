import json

import pytest

from tools import autopilot_development as worker


def test_curated_scope(tmp_path):
    path = tmp_path / "queue.json"
    path.write_text(json.dumps([{"id": "a", "role": "coder", "task_file": "../secret.md"}]))
    with pytest.raises(ValueError):
        worker.load_queue(path)


def test_queue_runs_proposal_only(tmp_path, monkeypatch):
    root = tmp_path
    (root / ".tasks").mkdir()
    (root / ".context").mkdir()
    queue = root / ".tasks/queue.json"
    queue.write_text(json.dumps([{"id": "a", "role": "coder", "task_file": ".tasks/a.md"}]))
    monkeypatch.setattr(worker, "ROOT", root)
    monkeypatch.setattr(worker, "STATE", root / ".context/state.json")
    monkeypatch.setattr(worker, "STOP", root / ".context/stop")
    monkeypatch.setattr(worker, "LOCK", root / ".context/lock")
    calls = []

    def fake_delegate(path, role, timeout):
        calls.append((path, role))
        return root / ".tasks/result.json"

    monkeypatch.setattr(worker, "delegate", fake_delegate)
    worker.run(queue, False, 1, 1)
    assert len(calls) == 1
    assert json.loads(worker.STATE.read_text())["jobs"]["a"] == "needs_orchestrator_review"
    assert not (root / "src").exists()
    worker.run(queue, False, 1, 1)
    assert len(calls) == 1
