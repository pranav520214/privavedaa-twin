"""Chronological sequential refitting, with no reuse of a posterior as a prior."""

from dataclasses import dataclass, field

import numpy as np

from transplant_twin.bayes.inference import Posterior, SamplingConfig, fit
from transplant_twin.pk.base import FloatArray
from transplant_twin.pk.population import SyntheticPopulation


@dataclass
class AdaptiveTwin:
    model: SyntheticPopulation
    config: SamplingConfig
    times: list[float] = field(default_factory=list, init=False)
    values: list[float] = field(default_factory=list, init=False)
    posterior: Posterior = field(init=False)

    def __post_init__(self) -> None:
        self.posterior = fit(
            self.model, np.array([], dtype=np.float64), np.array([], dtype=np.float64), self.config
        )

    def update(self, time: float, value: float) -> Posterior:
        if not np.isfinite(time) or not np.isfinite(value) or time < 0 or value <= 0:
            raise ValueError("Invalid synthetic observation")
        if self.times and time <= self.times[-1]:
            raise ValueError("Updates must be strictly later; duplicates are rejected")
        times, values = [*self.times, time], [*self.values, value]
        candidate = fit(
            self.model,
            np.array(times, dtype=np.float64),
            np.array(values, dtype=np.float64),
            self.config,
        )
        self.times, self.values, self.posterior = times, values, candidate
        return candidate

    def predict(self, horizon: float, seed: int, points: int = 24) -> FloatArray:
        if not np.isfinite(horizon) or horizon <= 0 or not 2 <= points <= 200:
            raise ValueError("Invalid research horizon")
        from transplant_twin.simulation.posterior_predictive import predictive_samples

        start = self.times[-1] if self.times else 0.0
        times = np.linspace(start, start + horizon, points, dtype=np.float64)
        return predictive_samples(self.model, self.posterior, times, seed)[1]
