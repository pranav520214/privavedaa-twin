import numpy as np

from transplant_twin.simulation.synthetic_patient import generate_patient


def test_seeded_truth_and_timeline():
    a, b = generate_patient(42), generate_patient(42)
    np.testing.assert_array_equal(a.values, b.values)
    assert a.truth == b.truth
    assert a.timeline == b.timeline
    assert a.truth != generate_patient(43).truth
    assert len(a.values) == 12
    assert all(o.provenance.synthetic for o in a.timeline.observations)
    assert np.all(a.values > 0)
