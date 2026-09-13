# Architecture and phase plan

An offline synthetic research platform, with a replaceable PopulationPKModel protocol.
Domain schemas -> validated timeline -> synthetic simulator -> Bayesian posterior ->
predictive samples -> temporally withheld evaluation -> labeled API/dashboard.
DuckDB stores research artifacts and reproducibility metadata, never direct identifiers.

0. Environment: empty directory, Python 3.12 available; Ollama 0.34.0 reachable.
   Hardware: 16.2 GB RAM, GTX 1650 4 GB, 257 GB disk free at inspection.
1. Delegation protocol first, smoke task reviewed/tested; package and strict schemas.
2. Synthetic one-compartment oral model with arbitrary demo parameters and known truth.
3. PyMC inference; estimate clearance with other synthetic parameters explicitly fixed
   to avoid pretending oral data identify clearance, volume and bioavailability separately.
4. Sequential refits to all earlier data, never posterior-as-prior plus reused data.
5. Patient-disjoint splits, fixed future holdout, M0/M1 comparisons and calibration.
6. Seeded sampling, global sensitivity, expected information gain, neutral scenarios.
7. Mock-only extraction candidates with explicit research review before timeline entry.
8. Versioned synthetic-only API and seven-page Streamlit dashboard.
9. Numerical, property, safety, integration checks and honest limitations.

Each major phase must pass gates before promotion. Real tacrolimus implementation
blocked until equations, units, covariates, population variability and residual error
parameters from a reproducible publication are independently verified.
