# Architecture

## Simple explanation
The simulator makes a virtual experiment with a known answer. The Bayesian model sees
only early measurements, then predicts measurements held back for evaluation.

## Technical explanation
Strict domain records feed a replaceable population model. A synthetic oral one-compartment
model supplies a controlled truth. Posterior samples propagate to predictive samples,
including observation noise. Deterministic metrics evaluate fixed temporal targets.

## Why we need it
Separating extraction, equations, inference and evaluation makes mistakes easier to find.
An LLM never sets the final metrics, changes the equations or approves extracted records.

## Implementation
`tools/` holds proposal-only local delegation; `src/transplant_twin/` holds the scientific
and service modules. `.tasks/` captures bounded work, `.context/` architecture and gates.
The API is restricted to server-generated synthetic cohorts.

## Tests
Schema rejection, independent numerical references, Bayesian recovery, temporal leakage,
reproducibility and output-label checks form the acceptance gates.
