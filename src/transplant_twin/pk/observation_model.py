"""Reviewed local-worker lognormal likelihood, including the density Jacobian."""

import numpy as np

from transplant_twin.pk.base import FloatArray


def lognormal_log_likelihood(values: FloatArray, predicted: FloatArray, sigma: float) -> float:
    if values.ndim != 1 or values.shape != predicted.shape or not len(values):
        raise ValueError("Expected matching nonempty vectors")
    if not np.all(np.isfinite(values)) or not np.all(np.isfinite(predicted)):
        raise ValueError("Concentrations must be finite")
    if np.any(values <= 0) or np.any(predicted <= 0):
        raise ValueError("Lognormal concentrations must be positive")
    if isinstance(sigma, bool) or not np.isfinite(sigma) or sigma <= 0:
        raise ValueError("Log-scale noise must be finite and positive")
    with np.errstate(over="ignore"):
        diff = (np.log(values) - np.log(predicted)) / sigma
        terms = -np.log(values) - np.log(sigma) - 0.5 * np.log(2 * np.pi) - 0.5 * diff**2
    # -inf is a valid log density for numerically negligible likelihood, not NaN.
    return float(np.sum(terms))
