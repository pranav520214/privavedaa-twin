import numpy as np
import pytest
from scipy.stats import lognorm

from transplant_twin.pk.observation_model import lognormal_log_likelihood


def test_density_against_scipy():
    values, predicted = np.array([1.0, 2.0, 4.0]), np.array([1.1, 2.3, 3.8])
    assert lognormal_log_likelihood(values, predicted, 0.15) == pytest.approx(
        lognorm.logpdf(values, s=0.15, scale=predicted).sum()
    )


@pytest.mark.parametrize("value", [0.0, -1.0, float("nan"), float("inf")])
def test_invalid_likelihood(value):
    with pytest.raises(ValueError):
        lognormal_log_likelihood(np.array([value]), np.array([1.0]), 0.15)


def test_empty_likelihood():
    with pytest.raises(ValueError):
        lognormal_log_likelihood(np.array([]), np.array([]), 0.15)
