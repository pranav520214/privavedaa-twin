# Adaptive transplant digital twin research platform

**RESEARCH SIMULATION — NOT FOR CLINICAL DECISION-MAKING.**

This project evaluates whether sequential Bayesian updating improves predictions of
withheld synthetic pharmacokinetic observations compared with a static population prior.
It does not recommend medicines, compute real patient doses, or establish clinical validity.

The initial model uses arbitrary synthetic parameters. No published tacrolimus model
has been independently reproduced here. See [scientific scope](docs/scientific_scope.md).

## Setup

Python 3.12+ is required. From this directory on Windows:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python -m pip install -e ".[bayes,ui,dev]"
.venv\Scripts\python -m pytest
.venv\Scripts\ruff check .
.venv\Scripts\ruff format --check .
.venv\Scripts\mypy src/ tools/
```

Ollama is optional for running the scientific core. It is used for bounded development
proposals, never for numerical calculations. See [local workers](docs/ollama_agents.md).
Implementation status and evidence are maintained in `.context/phase_gates.md`.
