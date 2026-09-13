# Bayesian synthetic twin

## Simple explanation
We start with a range of plausible virtual clearances. Each measurement changes how
plausible they are. Predictions average over this uncertainty rather than using one number.

## Technical explanation
The intended initial likelihood is log(y) ~ Normal(log(C(theta)), sigma). Clearance has a
lognormal population prior; volume, absorption, bioavailability and noise are known in
this controlled synthetic recovery experiment. This conditional setup is not a full
transplant population model. Sequential updates refit the original prior using all past
observations once, avoiding double counting.

## Why we need it
Point estimates hide ambiguity. Posterior samples allow latent credible intervals and
noisy prediction intervals to be distinguished. More data need not always narrow intervals.

## Implementation
PyMC is the inference backend. Use four independent chains for research runs,
retain samples and ArviZ diagnostics, and flag insufficient ESS, large R-hat or divergences.
The one-dimensional demonstration uses Slice sampling with the already-validated numerical
likelihood. Slice does not have HMC divergence diagnostics; that field remains null and
the sampler is explicitly named. Convergence requires finite R-hat <=1.01 and bulk/tail
ESS >=400. Short demonstration runs may legitimately remain marked needs_review.
Computation rejects log clearance outside (-20,20), a documented numerical support bound
far beyond this synthetic prior's meaningful mass. It is not a medical parameter range.
No posterior is declared converged merely because sampling completed.
Reference: https://www.pymc.io/projects/docs/en/stable/api/generated/pymc.sample.html

## Tests
Recover known synthetic clearance, compare with deterministic one-dimensional numerical
posterior integration, check seeded predictions, and evaluate withheld future observations.
A failed convergence diagnostic must remain visible in API/storage outputs.
