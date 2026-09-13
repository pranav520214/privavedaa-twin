import numpy as np
import pytest

from transplant_twin.validation.calibration import calibration_table
from transplant_twin.validation.metrics import metrics
from transplant_twin.validation.splitting import LockedTestGate, SplitManifest, patient_split
from transplant_twin.validation.temporal_holdout import temporal_holdout


def test_patient_groups_and_lock():
    split = patient_split([str(n) for n in range(10)] * 2, 42)
    assert split == patient_split([str(n) for n in range(10)], 42)
    assert len(split.development | split.validation | split.locked_test) == 10
    with pytest.raises(ValueError):
        SplitManifest(frozenset({"a"}), frozenset({"a"}), frozenset({"b"}), 42)
    with pytest.raises(ValueError):
        split.require_development(set(split.locked_test))
    gate = LockedTestGate(split)
    with pytest.raises(PermissionError):
        gate.access("calibration")
    assert gate.access("final_evaluation", True) == split.locked_test
    assert len(gate.events) == 1


def test_temporal_withholding():
    times, values = np.arange(1.0, 7.0), np.ones(6)
    a = temporal_holdout(times, values, 3.0)
    values[3:] = 999
    b = temporal_holdout(times, values, 3.0)
    np.testing.assert_array_equal(a.train_values, b.train_values)
    assert a.train_times.max() < a.test_times.min()
    assert not np.array_equal(a.test_values, b.test_values)


def test_known_metrics_and_calibration():
    actual = np.array([1.0, 3.0])
    samples = np.array([[0.0, 2.0], [2.0, 4.0]])
    result = metrics(actual, samples, np.log(np.full((2, 2), 0.25)))
    assert result["mae"] == result["rmse"] == result["bias"] == 0
    assert result["coverage_95"] == 1
    assert result["width_95"] == pytest.approx(1.9)
    assert result["nlpd"] == pytest.approx(np.log(4))
    assert calibration_table(actual, samples)[-1]["coverage"] == 1
    assert metrics(np.array([0.0, 3.0]), samples, np.zeros((2, 2)))["mdape"] is None
    with pytest.raises(ValueError):
        metrics(np.ones(1), samples, np.zeros((2, 2)))
