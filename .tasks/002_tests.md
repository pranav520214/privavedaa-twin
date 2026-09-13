{"task_id":"002_tests","context_type":"synthetic_or_code","allowed_files":["tests/unit/test_units.py"]}
Write pytest tests ONLY for from transplant_twin.domain.units import convert.
Interface convert(value:float, source:str, target:str)->float.
Valid mass mg µg ng; concentration mg/L ng/mL. Mismatched dimensions/unknown and nonfinite numbers raise ValueError.
Tests: 1 mg -> 1000 µg, 1mg -> 1000000ng, 1mg/L ->1000ng/mL; reverse; mass-concentration rejects; unknown rejects; NaN/Inf rejects. Use pytest.approx. Full file content; empty patch.
