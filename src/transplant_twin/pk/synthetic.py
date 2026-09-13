"""Synthetic oral mass-balance model, never a verified tacrolimus parameterization.

Local worker proposal reviewed and corrected: absorption multiplier, parameter validation,
full ODE trajectory, array shapes, finite outputs and equal-rate numerical stability.
"""

from dataclasses import dataclass, fields
from math import isfinite

import numpy as np
from scipy.integrate import solve_ivp

from transplant_twin.pk.base import FloatArray

MODEL_VERSION = "synthetic-oral-1c-v1"
MODEL_METADATA = {
    "version": MODEL_VERSION,
    "source": "arbitrary synthetic demonstration",
    "published_drug_model": False,
    "concentration_unit": "ng/mL",
}


@dataclass(frozen=True)
class Parameters:
    """Arbitrary demo values: CL L/h, V L, ka 1/h, F fraction, sigma log SD."""

    clearance: float = 4.0
    volume: float = 40.0
    absorption: float = 1.0
    bioavailability: float = 0.5
    sigma: float = 0.15

    def __post_init__(self) -> None:
        for field in fields(self):
            value = getattr(self, field.name)
            if isinstance(value, bool) or not isfinite(value) or value <= 0:
                raise ValueError(f"{field.name} must be finite and strictly positive")
        if self.bioavailability > 1:
            raise ValueError("Bioavailability must be at most one")
        if not isfinite(self.clearance / self.volume):
            raise ValueError("Elimination rate is not numerically representable")


def valid_vector(value: FloatArray, name: str) -> None:
    if value.ndim != 1 or not np.all(np.isfinite(value)):
        raise ValueError(f"{name} must be a finite one-dimensional array")


def concentration(
    times: FloatArray, p: Parameters, exposure_times: FloatArray, amounts: FloatArray
) -> FloatArray:
    """Analytic superposition, mg and L converted explicitly to ng/mL."""
    for array, name in ((times, "times"), (exposure_times, "exposure_times"), (amounts, "amounts")):
        valid_vector(array, name)
    if len(exposure_times) != len(amounts):
        raise ValueError("Exposure times and amounts must have equal lengths")
    if np.any(times < 0) or np.any(exposure_times < 0) or np.any(amounts <= 0):
        raise ValueError("Times must be nonnegative and exposure amounts positive")
    k, ka = p.clearance / p.volume, p.absorption
    result = np.zeros(times.shape, dtype=np.float64)
    for time, amount in zip(exposure_times, amounts, strict=True):
        mask = times >= time
        elapsed = times[mask] - time
        gap = abs(ka - k)
        # Factoring the slower exponential and using expm1 avoids subtraction loss
        # and never evaluates a growing exponential for ka < k.
        with np.errstate(over="ignore", under="ignore", invalid="ignore", divide="ignore"):
            if gap == 0:
                term = ka * elapsed * np.exp(-k * elapsed)
            else:
                term = ka * np.exp(-min(k, ka) * elapsed) * (-np.expm1(-gap * elapsed)) / gap
            result[mask] += 1000.0 * p.bioavailability * amount / p.volume * term
    if not np.all(np.isfinite(result)):
        raise ValueError("Concentration exceeds supported numerical range")
    return result


def ode_concentration(
    times: FloatArray, p: Parameters, exposure_time: float = 0.0, amount: float = 1.0
) -> FloatArray:
    """Independent one-exposure gut/central ODE reference, returning every requested time."""
    valid_vector(times, "times")
    if not isfinite(exposure_time) or exposure_time < 0 or not isfinite(amount) or amount <= 0:
        raise ValueError("Invalid exposure")
    if np.any(np.diff(times) <= 0) or np.any(times < exposure_time):
        raise ValueError("ODE times must be strictly ordered at or after exposure")
    if not len(times) or times[-1] == exposure_time:
        return np.zeros(times.shape, dtype=np.float64)

    def derivative(_time: float, state: FloatArray) -> list[float]:
        gut, central = state
        return [
            -p.absorption * float(gut),
            p.absorption * float(gut) - p.clearance / p.volume * float(central),
        ]

    solution = solve_ivp(
        derivative,
        (exposure_time, float(times[-1])),
        [p.bioavailability * amount, 0.0],
        t_eval=times,
        rtol=1e-10,
        atol=1e-12,
    )
    if not solution.success:
        raise RuntimeError(f"ODE reference failed: {solution.message}")
    result = np.asarray(solution.y[1] / p.volume * 1000.0, dtype=np.float64)
    if not np.all(np.isfinite(result)):
        raise ValueError("ODE solution is nonfinite")
    return result
