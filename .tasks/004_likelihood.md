{"task_id":"004_likelihood","context_type":"synthetic_or_code","allowed_files":["src/transplant_twin/pk/observation_model.py"]}
Write one small typed module: numpy np and scipy.special no other project imports.
def lognormal_log_likelihood(values: NDArray[np.float64], predicted: NDArray[np.float64], sigma: float) -> float.
Require same nonempty 1D shape; all values/predicted strictly positive finite; sigma finite>0. Raise ValueError on invalid. Formula sum[-log(values)-log(sigma)-.5log(2pi)-.5*((log(values)-log(predicted))/sigma)**2]. Include Jacobian -log(values) for lognormal density. Return Python float. Do not generate tests code in tests_proposed, only concise descriptions. Complete code content, empty patch.
