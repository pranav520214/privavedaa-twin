"""Synthetic implementation of the population-model protocol."""

from dataclasses import dataclass, replace

import numpy as np

from transplant_twin.pk.base import FloatArray
from transplant_twin.pk.observation_model import lognormal_log_likelihood
from transplant_twin.pk.synthetic import MODEL_VERSION, Parameters, concentration


@dataclass(frozen=True)
class SyntheticPopulation:
    exposure_times: FloatArray
    amounts: FloatArray
    fixed: Parameters = Parameters()
    model_version: str = MODEL_VERSION

    def __post_init__(self) -> None:
        times = np.array(self.exposure_times, dtype=np.float64, copy=True)
        amounts = np.array(self.amounts, dtype=np.float64, copy=True)
        concentration(np.array([], dtype=np.float64), self.fixed, times, amounts)
        times.setflags(write=False)
        amounts.setflags(write=False)
        object.__setattr__(self, "exposure_times", times)
        object.__setattr__(self, "amounts", amounts)

    def simulate(self, times: FloatArray, clearance: float) -> FloatArray:
        return concentration(
            times, replace(self.fixed, clearance=clearance), self.exposure_times, self.amounts
        )

    def log_likelihood(self, times: FloatArray, values: FloatArray, clearance: float) -> float:
        return lognormal_log_likelihood(values, self.simulate(times, clearance), self.fixed.sigma)

    def parameter_priors(self) -> dict[str, float | str]:
        return {
            "parameter": "clearance",
            "distribution": "lognormal",
            "log_mean": float(np.log(4.0)),
            "log_sd": 0.5,
            "scope": "arbitrary synthetic population prior",
        }
