{"task_id":"004_tests_review","context_type":"synthetic_or_code","allowed_files":[]}
Review Bayesian integration; propose at most 3 test cases and 3 concise risks. No file edits.
Only log clearance is unknown: Normal(log4,.5) prior. Numerical lognormal likelihood is a PyTensor as_op in PyMC Potential. PyMC Slice samples four chains cores1. Refit original prior on all chronological observations for each update. No ground-truth clearance passed into fit; known synthetic V,ka,F,sigma are fixed by design.
Posterior stores chain x draw samples, sampling seed/config, Rhat bulk/tail ESS, and in-sample posterior predictive coverage. Convergence iff finite Rhat<=1.01 and ESS>=400. Slice divergence field null, never pretending HMC. Prediction draws include independent lognormal noise.
Acceptance tests: independent 2401-point log-clearance quadrature mean vs posterior within2.5%; known synthetic truth in95% interval for fixed seed42; seeded predictive equality; noisy distribution wider than latent; chronological update count0,1,2; duplicate rejected.
All metrics are computed in Python. Does this avoid double counting and ground truth leakage? State only concrete findings.
