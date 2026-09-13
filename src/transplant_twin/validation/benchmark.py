"""M0 and M1 on identical fixed future synthetic observations."""

import numpy as np
from scipy.stats import lognorm

from transplant_twin.bayes.inference import SamplingConfig, fit
from transplant_twin.pk.population import SyntheticPopulation
from transplant_twin.safety.output_labels import RESEARCH_LABEL
from transplant_twin.simulation.posterior_predictive import predictive_samples, summarize
from transplant_twin.simulation.synthetic_patient import generate_patient
from transplant_twin.validation.calibration import calibration_table
from transplant_twin.validation.metrics import metrics
from transplant_twin.validation.temporal_holdout import temporal_holdout


def benchmark(
    seed: int, counts: tuple[int, ...] = (0, 1, 3, 6, 9), draws: int = 600, tune: int = 600
) -> dict[str, object]:
    if not counts or any(
        isinstance(n, bool) or not isinstance(n, int) or not 0 <= n <= 9 for n in counts
    ):
        raise ValueError("Counts must use only the nine earlier synthetic observations")
    if len(set(counts)) != len(counts):
        raise ValueError("Observation counts must be unique")
    patient = generate_patient(seed)
    model = SyntheticPopulation(patient.exposure_times, patient.amounts)
    config = SamplingConfig(seed=seed, draws=draws, tune=tune)
    split = temporal_holdout(patient.times, patient.values, float(patient.times[8]))
    prior = fit(model, np.array([], dtype=np.float64), np.array([], dtype=np.float64), config)
    m0_latent, m0_samples = predictive_samples(model, prior, split.test_times, seed + 100)
    m0_density = np.asarray(lognorm.logpdf(split.test_values, s=model.fixed.sigma, scale=m0_latent))
    baseline = metrics(split.test_values, m0_samples, m0_density)
    rows: list[dict[str, object]] = []
    for count in counts:
        posterior = (
            prior
            if count == 0
            else fit(model, split.train_times[:count], split.train_values[:count], config)
        )
        latent, samples = predictive_samples(model, posterior, split.test_times, seed + 100)
        density = np.asarray(lognorm.logpdf(split.test_values, s=model.fixed.sigma, scale=latent))
        rows.append(
            {
                "n_observations": count,
                "M0": baseline,
                "M1": metrics(split.test_values, samples, density),
                "prediction": summarize(samples),
                "calibration": calibration_table(split.test_values, samples),
                "diagnostics": posterior.diagnostics.model_dump(),
                "clearance_interval_width": float(
                    np.diff(np.quantile(posterior.clearance, [0.025, 0.975]))[0]
                ),
                "posterior_clearance": posterior.clearance.tolist(),
            }
        )
    return {
        "label": RESEARCH_LABEL,
        "seed": seed,
        "model_version": model.model_version,
        "sampling_config": config.model_dump(),
        "fixed_nuisance_parameters": {
            "volume": model.fixed.volume,
            "absorption": model.fixed.absorption,
            "bioavailability": model.fixed.bioavailability,
            "sigma": model.fixed.sigma,
        },
        "test_times": split.test_times.tolist(),
        "test_values": split.test_values.tolist(),
        "rows": rows,
        "scope": "single synthetic patient; no superiority or calibration claim",
    }
