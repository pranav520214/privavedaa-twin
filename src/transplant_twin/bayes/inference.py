"""PyMC inference conditional on explicitly known synthetic nuisance parameters."""

from dataclasses import dataclass
from typing import Literal

import numpy as np
from pydantic import Field

from transplant_twin.domain.models import StrictRecord
from transplant_twin.pk.base import FloatArray
from transplant_twin.pk.population import SyntheticPopulation


class SamplingConfig(StrictRecord):
    draws: int = Field(default=1000, ge=100, le=4000)
    tune: int = Field(default=1000, ge=100, le=4000)
    chains: int = Field(default=4, ge=2, le=4)
    seed: int = Field(ge=0, le=2**32 - 1)


class Diagnostics(StrictRecord):
    status: Literal["prior", "converged", "needs_review"]
    r_hat: float | None
    ess_bulk: float | None
    ess_tail: float | None
    sampler: str
    divergences: int | None = None
    notes: str


@dataclass(frozen=True)
class Posterior:
    clearance: FloatArray  # chains x draws, retained rather than only a point estimate
    diagnostics: Diagnostics
    config: SamplingConfig
    n_observations: int
    ppc_coverage: float | None


def fit(
    model: SyntheticPopulation, times: FloatArray, values: FloatArray, config: SamplingConfig
) -> Posterior:
    if times.ndim != 1 or times.shape != values.shape or not np.all(np.isfinite(times)):
        raise ValueError("Observation arrays must be finite matching vectors")
    if np.any(np.diff(times) <= 0):
        raise ValueError("Fit observations must be strictly chronological")
    if not len(times):
        samples = np.random.default_rng(config.seed).lognormal(
            np.log(4.0), 0.5, (config.chains, config.draws)
        )
        return Posterior(
            samples,
            Diagnostics(
                status="prior",
                r_hat=None,
                ess_bulk=None,
                ess_tail=None,
                sampler="independent population prior",
                notes="No observations; no MCMC convergence claim.",
            ),
            config,
            0,
            None,
        )
    # Validate data outside the probabilistic callback. Invalid records must never be
    # mistaken for low posterior probability.
    model.log_likelihood(times, values, 4.0)
    import arviz as az
    import pymc as pm
    import pytensor.tensor as pt
    from pytensor.compile.ops import as_op

    def log_likelihood(log_clearance: FloatArray) -> FloatArray:
        theta = float(log_clearance)
        # Finite computational support far beyond synthetic prior mass.
        if not np.isfinite(theta) or not -20 < theta < 20:
            return np.asarray(-np.inf, dtype=np.float64)
        try:
            result = model.log_likelihood(times, values, float(np.exp(theta)))
        except ValueError:
            result = -np.inf
        return np.asarray(result, dtype=np.float64)

    likelihood_op = as_op(itypes=[pt.dscalar], otypes=[pt.dscalar])(log_likelihood)
    with pm.Model():
        log_cl = pm.Normal("log_clearance", mu=float(np.log(4.0)), sigma=0.5)
        pm.Potential("observations", likelihood_op(log_cl))
        idata = pm.sample(
            draws=config.draws,
            tune=config.tune,
            chains=config.chains,
            cores=1,
            random_seed=config.seed,
            step=pm.Slice(),
            progressbar=False,
            return_inferencedata=True,
            compute_convergence_checks=True,
        )
    samples = np.asarray(np.exp(idata.posterior["log_clearance"].values), dtype=np.float64)
    summary = az.summary(idata, var_names=["log_clearance"], round_to="none")
    rhat, bulk, tail = (
        float(summary.loc["log_clearance", name]) for name in ("r_hat", "ess_bulk", "ess_tail")
    )
    finite = all(np.isfinite(x) for x in (rhat, bulk, tail))
    converged = finite and rhat <= 1.01 and bulk >= 400 and tail >= 400
    diagnostics = Diagnostics(
        status="converged" if converged else "needs_review",
        r_hat=rhat if np.isfinite(rhat) else None,
        ess_bulk=bulk if np.isfinite(bulk) else None,
        ess_tail=tail if np.isfinite(tail) else None,
        sampler="PyMC Slice, log clearance, cores=1",
        notes=(
            "Divergences do not apply to Slice. Conditional on known synthetic nuisance parameters."
        ),
    )
    latent = np.array([model.simulate(times, float(cl)) for cl in samples.ravel()])
    predictive = latent * np.exp(
        np.random.default_rng(config.seed + 1).normal(0.0, model.fixed.sigma, latent.shape)
    )
    lower, upper = np.quantile(predictive, [0.025, 0.975], axis=0)
    coverage = float(np.mean((values >= lower) & (values <= upper)))
    samples.setflags(write=False)
    return Posterior(samples, diagnostics, config, len(times), coverage)
