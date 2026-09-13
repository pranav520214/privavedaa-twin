# Validation protocol

## Simple explanation
The model sees early measurements. Later measurements are hidden until we score its
predictions. The same person must not appear on both sides of a patient-level split.

## Technical explanation
Development supports implementation/calibration. Validation supports model selection.
A locked patient-level test split is reserved for a final, explicitly requested evaluation.
Temporal holdout is a second boundary within each patient: future observations are never
included in posterior fitting. Compare M0 (the unchanged population prior) against M1
(the same prior adapted with earlier observations) on identical held-out targets.

## Why we need it
Using future information in fitting creates misleadingly good accuracy. Splitting rows
at random can leak information about a patient between evaluation groups.

## Implementation contract
An immutable manifest records patient group membership and seed. Overlap is rejected.
Locked-test access requires a separate explicit final-evaluation action and records that
the lock was opened. This is an auditable workflow, not protection against a local owner
editing files. Any later model change invalidates the final-test interpretation.
The synthetic benchmark uses fixed future targets at each observation count, reports all
results, and does not select favorable seeds or force M1 to outperform M0.

Metrics: MAE, RMSE, signed bias, MdAPE only for positive targets, prediction interval
coverage and width, and negative log predictive density from the predictive mixture.
Calibration is checked across multiple nominal coverage levels; small synthetic samples
do not establish population calibration. Repeated measurements are clustered by patient;
patient-level summaries are needed for independent uncertainty estimates.

## Tests
Check patient-disjoint partitions, strict time order and unchanged holdout targets.
Known small arrays verify metrics. Verify that changing withheld values does not change
the fit and that repeated seeds reproduce numerical artifacts.
