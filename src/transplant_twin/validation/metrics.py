"""Reviewed worker metrics; observation shape validation added by orchestrator."""

import numpy as np
from scipy.special import logsumexp

from transplant_twin.pk.base import FloatArray


def metrics(
    actual: FloatArray, samples: FloatArray, log_densities: FloatArray
) -> dict[str, float | None]:
    if actual.ndim != 1 or not len(actual) or samples.ndim != 2:
        raise ValueError("Expected observation vector and draws by observations matrix")
    if (
        samples.shape[0] < 2
        or samples.shape[1] != len(actual)
        or log_densities.shape != samples.shape
    ):
        raise ValueError("Predictive shapes do not match observations")
    if not all(np.all(np.isfinite(a)) for a in (actual, samples, log_densities)):
        raise ValueError("Metrics require finite data and evaluated log densities")
    error = np.median(samples, axis=0) - actual
    lower, upper = np.quantile(samples, [0.025, 0.975], axis=0)
    return {
        "mae": float(np.mean(np.abs(error))),
        "rmse": float(np.sqrt(np.mean(error**2))),
        "bias": float(np.mean(error)),
        "mdape": float(100 * np.median(np.abs(error / actual))) if np.all(actual > 0) else None,
        "coverage_95": float(np.mean((actual >= lower) & (actual <= upper))),
        "width_95": float(np.mean(upper - lower)),
        "nlpd": float(-np.mean(logsumexp(log_densities, axis=0) - np.log(samples.shape[0]))),
    }
