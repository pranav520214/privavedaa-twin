# Privavedaa Transplant Digital Twin Platform 🏥

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Code Quality: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type Checked: Mypy](https://img.shields.io/badge/type%20checker-mypy-blue.svg)](https://mypy-lang.org/)

> **Adaptive Synthetic Bayesian Pharmacokinetic Research Simulation Platform**

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⚠️ RESEARCH SIMULATION ONLY • NOT FOR CLINICAL USE • SYNTHETIC DATASETS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

> [!CAUTION]
> **RESEARCH SIMULATION ONLY — STRICTLY NON-CLINICAL**:  
> This project investigates mathematical hypotheses regarding whether sequential Bayesian updating improves predictions of withheld synthetic pharmacokinetic observations compared with a static population prior. It **does NOT** compute real patient doses, recommend medications, or claim clinical safety/efficacy. Initial simulations operate strictly on arbitrary synthetic parameters. See [Scientific Scope](docs/scientific_scope.md).

---

## ✨ Research Focus

1. **Sequential Bayesian Inference:** Evaluating Bayesian updating algorithms on non-linear synthetic pharmacokinetic curves (tacrolimus analog models).
2. **Prior vs. Posterior Convergence:** Measuring prediction error reduction as synthetic therapeutic drug monitoring (TDM) trough observations are iteratively ingested.
3. **Bounded Autopilot Development:** Proposal-only developer loop ensuring local worker models suggest changes without unsupervised repository mutation.

---

## 🏗️ Architecture

```text
🔬 Synthetic Population Prior
         │
         ▼
 ┌────────────────────────────────────────┐
 │   Bayesian Updating Engine (PyMC/MCMC) │ ◄── Withheld Synthetic Trough Data
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │     Posterior Parameter Estimation     │ ──► Clearance (CL) & Volume (Vd)
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │      Comparative Error Analysis        │ ──► Evaluation vs Static Prior
 └───────────────────┬────────────────────┘
                     │
                     ▼
 📋 Phase Gate Verification Ledger (.context/phase_gates.md)
```

---

## 🚀 Quick Start

### 1. Prerequisites
* Python 3.12+
* Optional: Local [Ollama](https://ollama.ai) instance for autopilot proposal generation

### 2. Installation & Verification
```bash
git clone https://github.com/pranav520214/privavedaa-twin.git
cd privavedaa-twin

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install with development dependencies
pip install -e ".[bayes,ui,dev]"

# Run quality checks
pytest
ruff check .
ruff format --check .
mypy src/ tools/
```

---

## 🤖 Bounded Autopilot Development

To execute the local proposal-only worker loop:
```powershell
.venv\Scripts\python tools\autopilot_development.py --watch --max-tasks 12
```

* Reads tasks from `.tasks/queue.json`.
* Submits scoped requests to local Ollama.
* Validates structured patches and writes proposals to `.tasks/results/`.
* **Zero autonomous mutation:** Patches require explicit human review to enter the codebase.

---

## 📚 Documentation
* [System Architecture](docs/architecture.md): Modular decomposition and data flow.
* [Bayesian Model Formulation](docs/bayesian_model.md): Priors, likelihoods, and parameter distributions.
* [Scientific Scope & Limitations](docs/scientific_scope.md): Ethical boundaries and model constraints.
* [Validation Protocol](docs/validation_protocol.md): Empirical test criteria and phase gate metrics.
* [Execution Flows](docs/flows.md): Sequential updating and proposal loops.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
