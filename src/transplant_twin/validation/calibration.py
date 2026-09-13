"""Empirical coverage tables for predictive observation samples."""

import numpy as np

from transplant_twin.pk.base import FloatArray


def calibration_table(actual: FloatArray, samples: FloatArray) -> list[dict[str, float]]:
    if actual.ndim != 1 or not len(actual) or samples.ndim != 2 or samples.shape[1] != len(actual):
        raise ValueError("Invalid calibration shapes")
    if samples.shape[0] < 2 or not all(np.all(np.isfinite(a)) for a in (actual, samples)):
        raise ValueError("Calibration requires finite samples")
    rows = []
    for nominal in (0.5, 0.8, 0.9, 0.95):
        lo, hi = np.quantile(samples, [(1 - nominal) / 2, (1 + nominal) / 2], axis=0)
        rows.append(
            {
                "nominal": nominal,
                "coverage": float(np.mean((actual >= lo) & (actual <= hi))),
                "mean_width": float(np.mean(hi - lo)),
            }
        )
    return rows
