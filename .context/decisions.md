# Decisions

- 2026-09-13: use available Python 3.12 instead of default Python 3.11.
- Use installed qwen2.5-coder:3b via loopback; no model downloads.
- Synthetic-only public endpoints; no real patient upload or dose optimization.
- Synthetic parameter values are arbitrary, not tacrolimus estimates.
- Original specification's information-gain typography is ambiguous: implement
  mutual information, i.e. expected KL(posterior || prior), equivalent to entropy
  difference (not an entropy ratio).
- Oral clearance/volume/bioavailability are confounded. First inference demonstration
  estimates clearance only conditional on known synthetic volume, absorption and F.
- Sequential uncertainty is measured, never forced to decrease.
