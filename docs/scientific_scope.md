# Scientific scope

RESEARCH SIMULATION — NOT FOR CLINICAL DECISION-MAKING.

## Simple explanation
A synthetic model is an invented laboratory experiment. Its numbers are not measurements
of tacrolimus in transplant recipients. Success here checks software, not clinical validity.

## Technical explanation
The demo uses an oral one-compartment mass-balance system with first-order absorption
and elimination. Its parameters are explicitly arbitrary. Clearance, volume, absorption,
bioavailability and residual noise are not sourced drug-specific estimates.

## Why we need it
Known latent truth allows recovery and predictive checks before handling real records.
Oral observations cannot generally identify absolute clearance, volume and bioavailability
independently. The initial inference fixes nuisance parameters to known synthetic truth.

## Implementation
Only clearance is adapted initially. Longitudinal synthetic covariates are recorded but
do not affect the equations until an explicit validated covariate model is supplied.
Prediction intervals include noise; latent credible intervals do not.

## Tests
Compare an analytic solution to an independent ODE integration, recover known clearance,
check finite values and units, and evaluate unseen future observations.

## Blocked real model
BLOCKER: no independently verified published tacrolimus parameterization.
WHY IT MATTERS: guessed equations or constants could falsely imply drug-specific validity.
WHAT IS REQUIRED: accessible original equations, parameter tables and units, covariate
definitions/centering, interindividual covariance, residual-error model, estimation
population, exposure formulation and independent reference trajectories.
WHAT CAN CONTINUE WITHOUT IT: all synthetic software, inference and evaluation infrastructure.

No synthetic result proves benefit in patients. External validation, governance and
independent scientific review remain future requirements.
