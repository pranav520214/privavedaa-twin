import math

from transplant_twin.domain.models import Observation


def convert(value: float, source: str, target: str) -> float:
    """
    Convert a value from one unit to another.

    Args:
        value (float): The value to convert.
        source (str): The source unit (e.g., 'mg', 'µg', 'ng', 'mg/L', 'ng/mL').
        target (str): The target unit (e.g., 'mg', 'µg', 'ng', 'mg/L', 'ng/mL').

    Returns:
        float: The converted value.

    Raises:
        ValueError: If the conversion is not possible or if the input values are NaN/Inf.
    """

    # Define conversion scales
    scales = {"mg": 1, "µg": 0.001, "ng": 0.000001, "mg/L": 1, "ng/mL": 0.001}

    # Validate input values
    if math.isnan(value) or math.isinf(value):
        raise ValueError("Input value cannot be NaN or Inf.")

    # Validate source and target units
    if source not in scales or target not in scales:
        raise ValueError("Unknown unit. Supported units are: mg, µg, ng, mg/L, ng/mL.")

    # Dimensions, not unit names, determine valid conversions.
    mass = {"mg", "µg", "ng"}
    if (source in mass) != (target in mass):
        raise ValueError("Cross-dimension conversion is not allowed.")

    # Perform conversion
    source_scale = scales[source]
    target_scale = scales[target]
    converted_value = value * source_scale / target_scale

    # Check if the result is finite
    if not math.isfinite(converted_value):
        raise ValueError("Conversion result is not finite.")

    return converted_value


def convert_observation(observation: "Observation", target: str) -> "Observation":
    """Convert explicitly and append provenance; missing values remain missing."""
    # Even missing records must have dimensionally valid conversions.
    convert(0.0, observation.unit, target)
    data = observation.model_dump()
    data["value"] = (
        None if observation.value is None else convert(observation.value, observation.unit, target)
    )
    data["unit"] = target
    data["provenance"]["transformations"] += (f"{observation.unit} -> {target}",)
    return Observation.model_validate(data)
