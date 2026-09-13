{"task_id":"004_integration","context_type":"synthetic_or_code","allowed_files":[]}
Orchestrator integration specification: combine validated synthetic model with local
likelihood proposal, PyMC Slice sampling of log clearance and ArviZ diagnostics.
Do not pass synthetic ground truth to fit; fixed nuisance parameters are explicit.
Original prior reused once on full chronological history. Store samples, seed, model,
sampler settings, diagnostics, and posterior predictive checks. Validate against independent
one-dimensional quadrature and synthetic clearance recovery. Scientific integration stays
with orchestrator because local numeric proposals have required substantial corrections.
