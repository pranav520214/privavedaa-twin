"""Population-model boundary; drug-specific implementations require verified sources."""

from typing import Protocol

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


class PopulationPKModel(Protocol):
    model_version: str

    def simulate(self, times: FloatArray, clearance: float) -> FloatArray: ...

    def log_likelihood(self, times: FloatArray, values: FloatArray, clearance: float) -> float: ...

    def parameter_priors(self) -> dict[str, float | str]: ...
