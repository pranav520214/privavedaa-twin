{"task_id":"002_review","context_type":"synthetic_or_code","allowed_files":[]}
Review the following design. Return concise findings in risks; no edits, empty files lists and patch.
Strict Pydantic records: extra forbid, strict true, allow_inf_nan false, AwareDatetime.
Observation value None iff missingness=='missing'; PK values >0 unit ng/mL; exposure values>=0 unit mg.
Timeline requires sorted timestamps and synthetic provenance if patient synthetic.
convert uses finite value; whitelist units and scales; mass={'mg','µg','ng'};
if (source in mass)!=(target in mass): raise ValueError. Else value*source_scale/target_scale.
scale mg=1, µg=.001, ng=.000001; mg/L=1, ng/mL=.001; output finite.
convert_observation calls conversion even on missing values, preserves source and appends transformation.
Tests reject NaN/Inf, missing mismatch, naive time, unordered records; conversion known factors and dimension rejection.
Are dimensions and missingness correct? What missing tests or safety issues remain? This is synthetic code only.
