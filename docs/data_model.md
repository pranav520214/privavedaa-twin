# Research data model

## Simple explanation
Each measurement says what was measured, when, in which units, and where it came from.
Missing measurements stay missing.

## Technical explanation
Pydantic records forbid extra fields, reject nonfinite values and require timezone-aware
timestamps. Numeric observations and categorical genotype observations are separate.
Missingness must match a null value. Timeline ordering is explicit; source metadata persists.

## Why we need it
Mass and concentration are different dimensions. Milligrams and nanograms differ by a
factor of one million; mg/L and ng/mL differ by a factor of one thousand.

## Implementation
Patients have research IDs only. PK observations use ng/mL, exposure records mg.
Conversion is explicit and adds an entry to transformation provenance. Generic laboratory
units may be retained as source labels, but numerical PK ingestion accepts only its whitelist.
Genotypes are categorical, never silently converted to numbers.

## Tests
Nonfinite input, missingness mismatch, naive timestamps, extra fields, dimensional mismatch,
unit round trips and out-of-order timelines are rejected or checked.
