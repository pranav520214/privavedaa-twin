# Phase gates

0 environment: inspected; no existing repository files or parent AGENTS.md, no Git repository.
1 foundation gate passed: 30 schema/unit/protocol/safety tests; strict mypy, Ruff and
format checks passed before phase 2 integration. Local smoke passed 3 assertions.
002_domain proposal REJECTED: truncated Python, invalid Pydantic imports, missing requested
file and schema invariants. JSON structural validity did not imply valid code. Splitting
worker tasks more narrowly; orchestrator will repair domain interfaces.
002_units: corrected worker's reversed dimension predicate; known-factor and rejection
tests pass. 002_tests: repaired missing pytest parameter fixtures with explicit cases.
002_review: first response rejected as truncated JSON. Bounded retry returned findings;
claims of missing validation were checked against existing tests and found inapplicable.
003_pk first response rejected as truncated JSON; retry uses installed qwen3.5:4b.
Phase 2 passed: analytic/ODE agreement across multiple parameter regimes, near-equal
rates, superposition, strict invalid inputs and seeded synthetic timeline. Worker test
proposals contained incorrect k=CL/V arithmetic and initial conditions; rejected.
Phase 3/4 passed: 53 total tests, including PyMC recovery versus 2401-point independent
quadrature, convergence gate, noisy/latent prediction distinction and chronological
updates. Full test run 38.42s on this host. Ruff and strict project type checks pass.
The dependency's as_op emits a deprecation warning; its suggested top-level wrap_py
replacement is absent in installed PyTensor. Current pinned functionality is tested.
Environment: NumPy 2.5.3 / Numba combination failed on removed np.row_stack. Pinning
NumPy 2.2.6 restored PyMC 5.28.5 import. Removed optional incompatible scipy-stubs;
uv pip check now reports all installed packages compatible.
Real drug model blocked as documented in docs/scientific_scope.md.
