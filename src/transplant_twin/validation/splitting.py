"""Patient grouping is explicit and a locked-test access leaves an audit event."""

from dataclasses import dataclass, field

import numpy as np


@dataclass(frozen=True)
class SplitManifest:
    development: frozenset[str]
    validation: frozenset[str]
    locked_test: frozenset[str]
    seed: int

    def __post_init__(self) -> None:
        if not all((self.development, self.validation, self.locked_test)):
            raise ValueError("All three patient groups must be nonempty")
        if (
            self.development & self.validation
            or self.development & self.locked_test
            or self.validation & self.locked_test
        ):
            raise ValueError("Patient identity groups overlap")

    def require_development(self, patient_ids: set[str]) -> None:
        if not patient_ids <= self.development:
            raise ValueError("Calibration is restricted to development patients")


def patient_split(patient_ids: list[str], seed: int) -> SplitManifest:
    unique = sorted(set(patient_ids))
    if len(unique) < 5 or any(not p for p in unique):
        raise ValueError("At least five nonempty research identities required")
    shuffled = np.random.default_rng(seed).permutation(unique).tolist()
    n = len(shuffled)
    development_end = max(1, int(0.6 * n))
    validation_end = min(n - 1, development_end + max(1, int(0.2 * n)))
    return SplitManifest(
        frozenset(shuffled[:development_end]),
        frozenset(shuffled[development_end:validation_end]),
        frozenset(shuffled[validation_end:]),
        seed,
    )


@dataclass
class LockedTestGate:
    manifest: SplitManifest
    events: list[str] = field(default_factory=list)

    def access(self, purpose: str, final_evaluation: bool = False) -> frozenset[str]:
        if not final_evaluation or purpose != "final_evaluation":
            raise PermissionError("Locked patients cannot be used for calibration or selection")
        self.events.append("locked_test_opened_for_final_evaluation")
        return self.manifest.locked_test
