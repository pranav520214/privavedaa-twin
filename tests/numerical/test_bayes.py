import numpy as np
import pytest
from scipy.special import logsumexp

from transplant_twin.bayes.inference import SamplingConfig, fit
from transplant_twin.bayes.twin import AdaptiveTwin
from transplant_twin.pk.population import SyntheticPopulation
from transplant_twin.simulation.posterior_predictive import predictive_samples
from transplant_twin.simulation.synthetic_patient import generate_patient


@pytest.fixture(scope="module")
def fitted():
    patient = generate_patient(42)
    model = SyntheticPopulation(patient.exposure_times, patient.amounts)
    config = SamplingConfig(draws=600, tune=600, chains=4, seed=42)
    posterior = fit(model, patient.times[:9], patient.values[:9], config)
    return patient, model, posterior


@pytest.mark.slow
def test_recovery_against_quadrature(fitted):
    patient, model, posterior = fitted
    grid = np.linspace(np.log(4.0) - 3.0, np.log(4.0) + 3.0, 2401)
    logweights = (
        np.array(
            [
                model.log_likelihood(patient.times[:9], patient.values[:9], float(np.exp(x)))
                for x in grid
            ]
        )
        - 0.5 * ((grid - np.log(4.0)) / 0.5) ** 2
    )
    weights = np.exp(logweights - logsumexp(logweights))
    expected = np.sum(np.exp(grid) * weights)
    assert float(np.mean(posterior.clearance)) == pytest.approx(expected, rel=0.025)
    lower, upper = np.quantile(posterior.clearance, [0.025, 0.975])
    assert lower < patient.truth.clearance < upper
    assert posterior.diagnostics.status == "converged"
    assert posterior.diagnostics.ess_bulk >= 400
    assert posterior.n_observations == 9
    assert posterior.ppc_coverage is not None


def test_predictive_seed_and_noise(fitted):
    patient, model, posterior = fitted
    latent, noisy = predictive_samples(model, posterior, patient.times[9:], 17)
    np.testing.assert_array_equal(
        noisy, predictive_samples(model, posterior, patient.times[9:], 17)[1]
    )
    assert not np.array_equal(noisy, predictive_samples(model, posterior, patient.times[9:], 18)[1])
    assert noisy.shape == latent.shape == (2400, 3)
    assert np.std(noisy[:, 0]) > np.std(latent[:, 0])


def test_prior_and_sequential_update():
    patient = generate_patient(42)
    twin = AdaptiveTwin(
        SyntheticPopulation(patient.exposure_times, patient.amounts),
        SamplingConfig(draws=100, tune=100, chains=2, seed=42),
    )
    assert twin.posterior.diagnostics.status == "prior"
    first = twin.update(float(patient.times[0]), float(patient.values[0]))
    assert first.n_observations == 1
    with pytest.raises(ValueError):
        twin.update(float(patient.times[0]), float(patient.values[0]))
    second = twin.update(float(patient.times[1]), float(patient.values[1]))
    assert second.n_observations == 2
    assert twin.predict(horizon=12.0, seed=4).shape == (200, 24)
