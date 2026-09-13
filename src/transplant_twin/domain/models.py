"""Strict research records with explicit missingness and lineage."""

from typing import Annotated, Literal, Self

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, model_validator

Text = Annotated[str, Field(min_length=1, max_length=200)]


class StrictRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False, strict=True)


class DataProvenance(StrictRecord):
    source: Text
    transformations: tuple[str, ...] = ()
    synthetic: bool


class Observation(StrictRecord):
    value: float | None
    unit: Text
    timestamp: AwareDatetime
    source: Text
    confidence: float = Field(ge=0, le=1)
    missingness: Literal["observed", "missing"]
    provenance: DataProvenance

    @model_validator(mode="after")
    def consistent_missingness(self) -> Self:
        if (self.value is None) != (self.missingness == "missing"):
            raise ValueError("Missingness must agree with value; no imputation is performed")
        return self


class LaboratoryMeasurement(Observation):
    analyte: Text


class PhysiologicalCovariate(Observation):
    name: Text


class GenotypeObservation(StrictRecord):
    value: Text | None
    unit: Literal["allele"] = "allele"
    timestamp: AwareDatetime
    source: Text
    confidence: float = Field(ge=0, le=1)
    missingness: Literal["observed", "missing"]
    provenance: DataProvenance

    @model_validator(mode="after")
    def consistent_missingness(self) -> Self:
        if (self.value is None) != (self.missingness == "missing"):
            raise ValueError("Missingness must agree with genotype value")
        return self


class PKObservation(Observation):
    unit: Literal["ng/mL"] = "ng/mL"
    value: float | None = Field(gt=0)


class MedicationExposureRecord(Observation):
    unit: Literal["mg"] = "mg"
    value: float | None = Field(ge=0)


class Patient(StrictRecord):
    research_id: Text
    synthetic: bool = True


ResearchObservation = (
    PKObservation
    | MedicationExposureRecord
    | LaboratoryMeasurement
    | PhysiologicalCovariate
    | GenotypeObservation
    | Observation
)


class PatientTimeline(StrictRecord):
    patient: Patient
    observations: tuple[ResearchObservation, ...]

    @model_validator(mode="after")
    def ordered(self) -> Self:
        times = [o.timestamp for o in self.observations]
        if times != sorted(times):
            raise ValueError("Timeline must be ordered by timestamp")
        if self.patient.synthetic and any(not o.provenance.synthetic for o in self.observations):
            raise ValueError("Synthetic timelines cannot contain non-synthetic records")
        return self
