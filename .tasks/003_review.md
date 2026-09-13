{"task_id":"003_review","context_type":"synthetic_or_code","allowed_files":[]}
Review synthetic numerical model. Max 3 concise risks. No files, empty patch.
Original local proposal omitted ka multiplier except equal-rate branch and returned only last ODE point; both repaired.
Current formula: gap=abs(ka-k); term=ka*exp(-min(k,ka)*t)*(-expm1(-gap*t))/gap, equal gap=0 uses ka*t*exp(-k*t). C=1000*F*amount/V*term. Only t>=0 evaluated; exposures superposed. Parameters positive finite, F<=1. Arrays finite 1D; nonnegative times; positive amounts; finite outputs.
Independent ODE: initial gut=F*amount, central=0, derivative [-ka*gut,ka*gut-k*central], solve_ivp t_eval=times from exposure time. rtol1e-10 atol1e-12. Return entire central/V*1000 trajectory.
Tests compare analytic at1h, equal-rate limit, ODE at ka1,.1,10,.001, pre-exposure zeros, repeated exposure sum, NaN/Inf, negative parameters; 43 project tests passed. Identify actual remaining issues only; no medical claims.
