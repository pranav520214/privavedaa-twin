"""Parameter uncertainty and observation noise are distinct distributions."""

import numpy as np

from transplant_twin.bayes.inference import Posterior
from transplant_twin.pk.base import FloatArray
from transplant_twin.pk.population import SyntheticPopulation


def predictive_samples(
    model: SyntheticPopulation, posterior: Posterior, times: FloatArray, seed: int
) -> tuple[FloatArray, FloatArray]:
    latent = np.array(
        [model.simulate(times, float(cl)) for cl in posterior.clearance.ravel()], dtype=np.float64
    )
    noisy = latent * np.exp(
        np.random.default_rng(seed).normal(0.0, model.fixed.sigma, latent.shape)
    )
    if not np.all(np.isfinite(noisy)):
        raise ValueError("Nonfinite predictive sample")
    return latent, noisy


def summarize(samples: FloatArray) -> dict[str, list[float]]:
    if samples.ndim != 2 or samples.shape[0] < 2 or not np.all(np.isfinite(samples)):
        raise ValueError("Expected finite draws by times matrix")
    lower, median, upper = np.quantile(samples, [0.025, 0.5, 0.975], axis=0)
    return {"lower": lower.tolist(), "median": median.tolist(), "upper": upper.tolist()}
