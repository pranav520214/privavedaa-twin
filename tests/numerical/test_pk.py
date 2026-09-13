from dataclasses import replace

import numpy as np
import pytest

from transplant_twin.pk.synthetic import Parameters, concentration, ode_concentration


def test_analytic_reference_and_limit():
    p = Parameters()
    t = np.array([0.0, 1.0, 12.0])
    c = concentration(t, p, np.array([0.0]), np.array([1.0]))
    expected = 1000 * 0.5 / 40 * (np.exp(-0.1 * t) - np.exp(-t)) / 0.9
    np.testing.assert_allclose(c, expected, rtol=1e-12)
    equal = replace(p, absorption=0.1)
    np.testing.assert_allclose(
        concentration(t, equal, np.array([0.0]), np.array([1.0])),
        12.5 * 0.1 * t * np.exp(-0.1 * t),
        rtol=1e-12,
    )


@pytest.mark.parametrize(
    "p",
    [
        Parameters(),
        Parameters(absorption=0.1),
        Parameters(clearance=0.01, absorption=10.0),
        Parameters(clearance=40.0, absorption=0.001),
    ],
)
def test_independent_ode(p):
    t = np.linspace(0, 48, 97)
    np.testing.assert_allclose(
        concentration(t, p, np.array([0.0]), np.array([1.0])),
        ode_concentration(t, p),
        rtol=2e-6,
        atol=1e-7,
    )


def test_exposure_timing_and_superposition():
    p = Parameters()
    t = np.array([0.0, 6.0, 12.0, 13.0, 24.0])
    a = concentration(t, p, np.array([12.0]), np.array([1.0]))
    assert np.all(a[:3] == 0)
    b = concentration(t, p, np.array([0.0]), np.array([1.0]))
    np.testing.assert_allclose(
        concentration(t, p, np.array([0.0, 12.0]), np.array([1.0, 1.0])), a + b
    )


@pytest.mark.parametrize(
    "changes",
    [
        {"clearance": 0.0},
        {"volume": -1.0},
        {"absorption": float("nan")},
        {"bioavailability": 1.1},
        {"sigma": float("inf")},
    ],
)
def test_invalid_parameters(changes):
    with pytest.raises(ValueError):
        Parameters(**changes)


def test_nearly_equal_rates():
    t = np.array([0.0, 1.0, 12.0, 100.0], dtype=np.float64)
    equal = concentration(t, Parameters(absorption=0.1), np.array([0.0]), np.array([1.0]))
    nearby = concentration(t, Parameters(absorption=0.1 + 1e-15), np.array([0.0]), np.array([1.0]))
    np.testing.assert_allclose(nearby, equal, rtol=1e-12, atol=1e-14)


def test_invalid_arrays():
    for times in [np.array([float("nan")]), np.array([-1.0]), np.array([[1.0]])]:
        with pytest.raises(ValueError):
            concentration(times, Parameters(), np.array([0.0]), np.array([1.0]))
    with pytest.raises(ValueError):
        concentration(np.array([1.0]), Parameters(), np.array([0.0, 12.0]), np.array([1.0]))
