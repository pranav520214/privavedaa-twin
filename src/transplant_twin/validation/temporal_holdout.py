"""Fixed future targets; early-count comparisons never move the evaluation window."""

from dataclasses import dataclass

import numpy as np

from transplant_twin.pk.base import FloatArray


@dataclass(frozen=True)
class TemporalHoldout:
    train_times: FloatArray
    train_values: FloatArray
    test_times: FloatArray
    test_values: FloatArray


def temporal_holdout(times: FloatArray, values: FloatArray, cutoff: float) -> TemporalHoldout:
    if times.ndim != 1 or times.shape != values.shape or not len(times):
        raise ValueError("Invalid longitudinal arrays")
    if not all(np.all(np.isfinite(a)) for a in (times, values)) or not np.isfinite(cutoff):
        raise ValueError("Nonfinite observations or cutoff")
    if np.any(np.diff(times) <= 0) or np.any(values <= 0):
        raise ValueError("Expected strictly chronological positive observations")
    earlier = times <= cutoff
    if not np.any(earlier) or np.all(earlier):
        raise ValueError("Temporal split needs both earlier and future observations")
    return TemporalHoldout(
        times[earlier].copy(),
        values[earlier].copy(),
        times[~earlier].copy(),
        values[~earlier].copy(),
    )
