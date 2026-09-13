"""Known synthetic truth; do not pass this object directly into inference."""

from dataclasses import dataclass, replace
from datetime import UTC, datetime, timedelta
from typing import Literal, TypedDict

import numpy as np

from transplant_twin.domain.models import (
    DataProvenance,
    MedicationExposureRecord,
    Patient,
    PatientTimeline,
    PhysiologicalCovariate,
    PKObservation,
)
from transplant_twin.pk.base import FloatArray
from transplant_twin.pk.synthetic import Parameters, concentration


class RecordMetadata(TypedDict):
    source: str
    confidence: float
    missingness: Literal["observed"]
    provenance: DataProvenance


@dataclass(frozen=True)
class SyntheticPatient:
    timeline: PatientTimeline
    truth: Parameters
    times: FloatArray
    values: FloatArray
    exposure_times: FloatArray
    amounts: FloatArray
    seed: int


def generate_patient(seed: int, research_id: str = "virtual-001") -> SyntheticPatient:
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
        raise ValueError("An explicit nonnegative integer seed is required")
    rng = np.random.default_rng(seed)
    truth = replace(Parameters(), clearance=float(rng.lognormal(np.log(4.0), 0.5)))
    times = np.arange(2.0, 74.0, 6.0, dtype=np.float64)
    exposure_times = np.arange(0.0, 73.0, 12.0, dtype=np.float64)
    amounts = np.ones(len(exposure_times), dtype=np.float64)
    latent = concentration(times, truth, exposure_times, amounts)
    values = latent * np.exp(rng.normal(0.0, truth.sigma, size=len(times)))
    epoch = datetime(2020, 1, 1, tzinfo=UTC)
    provenance = DataProvenance(source="seeded synthetic generator v1", synthetic=True)
    records: list[PKObservation | MedicationExposureRecord | PhysiologicalCovariate] = []
    common: RecordMetadata = dict(
        source="synthetic generator", confidence=1.0, missingness="observed", provenance=provenance
    )
    for time, value in zip(times, values, strict=True):
        records.append(
            PKObservation(
                value=float(value), timestamp=epoch + timedelta(hours=float(time)), **common
            )
        )
    for time, amount in zip(exposure_times, amounts, strict=True):
        records.append(
            MedicationExposureRecord(
                value=float(amount), timestamp=epoch + timedelta(hours=float(time)), **common
            )
        )
    for covariate_time in (0.0, 24.0, 48.0, 72.0):
        records.append(
            PhysiologicalCovariate(
                name="synthetic covariate (not in equations)",
                value=float(1.0 + 0.1 * np.sin(covariate_time / 24.0)),
                unit="dimensionless",
                timestamp=epoch + timedelta(hours=covariate_time),
                **common,
            )
        )
    timeline = PatientTimeline(
        patient=Patient(research_id=research_id),
        observations=tuple(sorted(records, key=lambda r: r.timestamp)),
    )
    for array in (times, values, exposure_times, amounts):
        array.setflags(write=False)
    return SyntheticPatient(timeline, truth, times, values, exposure_times, amounts, seed)
