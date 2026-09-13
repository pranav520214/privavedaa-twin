"""Worker-proposed cases, repaired to supply explicit inputs and expectations."""

import pytest

from tests.unit.test_domain import record
from transplant_twin.domain.models import Observation
from transplant_twin.domain.units import convert, convert_observation


@pytest.mark.parametrize(
    "value,source,target,expected",
    [
        (1.0, "mg", "µg", 1000.0),
        (1.0, "mg", "ng", 1e6),
        (1.0, "mg/L", "ng/mL", 1000.0),
        (1000.0, "ng/mL", "mg/L", 1.0),
        (1.0, "mg", "mg", 1.0),
    ],
)
def test_known_conversions(value, source, target, expected):
    assert convert(value, source, target) == pytest.approx(expected)


@pytest.mark.parametrize(
    "value,source,target",
    [
        (1.0, "mg", "mg/L"),
        (1.0, "ng/mL", "ng"),
        (1.0, "g", "mg"),
        (float("nan"), "mg", "mg"),
        (float("inf"), "mg", "mg"),
        (1e308, "mg", "ng"),
    ],
)
def test_invalid_conversions(value, source, target):
    with pytest.raises(ValueError):
        convert(value, source, target)


def test_provenance_and_missing_conversion():
    original = Observation(**record(unit="mg/L"))
    converted = convert_observation(original, "ng/mL")
    assert converted.value == 1000
    assert converted.provenance.transformations == ("mg/L -> ng/mL",)
    assert original.provenance.transformations == ()
    missing = Observation(**record(value=None, missingness="missing", unit="mg/L"))
    assert convert_observation(missing, "ng/mL").value is None
