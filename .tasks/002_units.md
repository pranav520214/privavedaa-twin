{"task_id":"002_units","context_type":"synthetic_or_code","allowed_files":["src/transplant_twin/domain/units.py"]}
Create ONLY a small unit conversion module. Python 3.12. Full code in content.
def convert(value: float, source: str, target: str) -> float.
Reject NaN/Inf, unknown units, and cross-dimension conversion with ValueError.
Mass scales relative to mg: mg=1, µg=.001, ng=.000001.
Concentration scales relative to mg/L: mg/L=1, ng/mL=.001.
Result=value*source_scale/target_scale. Check result is finite too.
No other files. Include a short docstring that the caller must retain transformation provenance.
Use math.isfinite; type annotations. No dependencies. Return all schema fields, patch empty.
