# Local coding workers

## Simple explanation
A local model proposes a small change. The orchestrator checks it before it enters the code.

## Technical explanation
The native loopback `/api/chat` endpoint receives a Pydantic JSON schema in `format`.
Responses are parsed again and checked against a file allowlist and task identifier.
Free-form patches are rejected. The tool never executes or applies worker output.
Reference: https://docs.ollama.com/capabilities/structured-outputs

## Why we need it
Structured output is not evidence that code is correct. Scope checks reduce accidental
repository changes; numerical tests remain the authority for mathematical behavior.

## Implementation
Inspect `ollama list`; configuration chooses among installed coding models. No automatic
downloads. This machine initially has qwen2.5-coder:3b and a 4 GB GPU.

```powershell
.venv\Scripts\python tools/ollama_delegate.py --role coder --task-file .tasks/001_smoke.md
```

The first line of each task is JSON metadata (`task_id`, `context_type`, `allowed_files`).
Only curated code/synthetic context is permitted. This assertion is a workflow boundary,
not an automatic detector of personal health information. Never include patient records.
Responses and audit hashes are stored in `.tasks/results/`. Review findings do not approve code.
If no coding model is installed, choose one after checking available memory/disk; the tool stops.

## Tests
Malformed JSON, missing fields, extra fields, path traversal, mismatched task ids,
out-of-scope files and non-loopback origins are rejected. A trivial addition proposal
was inspected, integrated, then checked on negative, zero and positive inputs.
