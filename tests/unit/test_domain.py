from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from transplant_twin.domain.models import (
    DataProvenance,
    Observation,
    Patient,
    PatientTimeline,
    PKObservation,
)


def record(**changes):
    return (
        dict(
            value=1.0,
            unit="ng/mL",
            timestamp=datetime(2020, 1, 1, tzinfo=UTC),
            source="synthetic",
            confidence=1.0,
            missingness="observed",
            provenance=DataProvenance(source="generator", synthetic=True),
        )
        | changes
    )


@pytest.mark.parametrize(
    "changes",
    [
        {"value": float("nan")},
        {"value": float("inf")},
        {"timestamp": datetime(2020, 1, 1)},
        {"value": None},
        {"missingness": "missing"},
        {"confidence": 1.1},
        {"unexpected": 1},
    ],
)
def test_invalid_record(changes):
    with pytest.raises(ValidationError):
        Observation(**record(**changes))


def test_missing_and_ordering():
    first = Observation(**record(value=None, missingness="missing"))
    second = Observation(**record(timestamp=first.timestamp + timedelta(hours=1)))
    patient = Patient(research_id="virtual-1")
    assert PatientTimeline(patient=patient, observations=(first, second))
    with pytest.raises(ValidationError):
        PatientTimeline(patient=patient, observations=(second, first))
    for value in [0.0, -1.0]:
        with pytest.raises(ValidationError):
            PKObservation(**record(value=value))
