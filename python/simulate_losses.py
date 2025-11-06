"""
simulate_losses.py
Monte Carlo for aggregate annual losses using:
- Frequency: Poisson or NegBin (from R frequency_model.R)
- Severity: Gamma or Lognormal (from R severity_model.R)
Fallback if severity fit fails: Lognormal with configurable mean/sd.

Outputs:
- results/simulated_losses.csv  (one column: loss)
- summary dict (printed) with mean, stdev, VaR95/99, TVaR95/99
"""

import os
import math
import numpy as np
import pandas as pd

from r_bridge import fit_frequency, fit_severity

# --- CONFIG ---
N_SIM = 50_000  # per your choice
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
RESULTS_PATH = os.path.join(RESULTS_DIR, "simulated_losses.csv")

# If severity model == "none", use this fallback (tweak to your domain)
FALLBACK_SEVERITY = {
    "type": "lognormal",  # 'lognormal' only in this fallback
    "mean": 20_000.0,     # average claim amount (USD)
    "sd": 30_000.0        # std dev of claim amount (USD)
}
# ---------------


def _ensure_dirs():
    os.makedirs(RESULTS_DIR, exist_ok=True)


def _sample_frequency(freq_params, size):
    model = freq_params.get("model")
    mu = float(freq_params.get("mu", 0.0) or 0.0)

    if model == "Poisson":
        return np.random.poisson(mu, size=size)

    if model == "NegBin":
        # MASS::glm.nb uses 'theta' as size; Var = mu + mu^2/theta
        theta = freq_params.get("theta", None)
        if theta is None or (isinstance(theta, float) and math.isnan(theta)):
            # degenerate, fall back to Poisson
            return np.random.poisson(mu, size=size)

        theta = float(theta)
        # Gamma-Poisson mixture: lambda ~ Gamma(shape=theta, scale=mu/theta), N~Pois(lambda)
        lam = np.random.gamma(shape=theta, scale=mu / theta, size=size)
        return np.random.poisson(lam)

    # unknown -> safe default
    return np.random.poisson(mu, size=size)


def _sample_severity_vector(n, sev_params):
    """Return a vector of n severities from the fitted model (or fallback)."""
    model = sev_params.get("model")

    if model == "gamma":
        shape = float(sev_params["gamma_shape"])
        rate = float(sev_params["gamma_rate"])  # R uses rate = 1/scale
        scale = 1.0 / rate
        return np.random.gamma(shape=shape, scale=scale, size=n)

    if model == "lognormal":
        meanlog = float(sev_params["ln_meanlog"])
        sdlog = float(sev_params["ln_sdlog"])
        return np.random.lognormal(mean=meanlog, sigma=sdlog, size=n)

    # Fallback (your severity fit returned 'none')
    if FALLBACK_SEVERITY["type"] == "lognormal":
        m = float(FALLBACK_SEVERITY["mean"])
        s = float(FALLBACK_SEVERITY["sd"])
        # Convert mean/stdev to lognormal params
        # If X~LogN(mu, sigma): mean = exp(mu + sigma^2/2), var = (exp(sigma^2)-1)exp(2mu+sigma^2)
        # Solve for mu, sigma from mean (m), stdev (s)
        var = s ** 2
        sigma2 = math.log(1.0 + var / (m ** 2))
        sigma = math.sqrt(sigma2)
        mu = math.log(m) - sigma2 / 2.0
        return np.random.lognormal(mean=mu, sigma=sigma, size=n)

    # Last-ditch: constant tiny severities (should never happen)
    return np.full(n, 1.0)


def run_simulation(n_sim: int = N_SIM, save_csv: bool = True):
    _ensure_dirs()

    freq_params = fit_frequency()
    sev_params = fit_severity()

    # Simulate claim counts per "year"
    counts = _sample_frequency(freq_params, size=n_sim)

    # For each simulated year, draw severities and sum
    losses = np.zeros(n_sim, dtype=float)
    # Fast path: if many zeros, skip
    nonzero_idx = np.nonzero(counts)[0]
    if nonzero_idx.size > 0:
        total_claims = int(counts[nonzero_idx].sum())
        # draw all severities at once, then partition
        severities_all = _sample_severity_vector(total_claims, sev_params)

        # assign blocks
        start = 0
        for i in nonzero_idx:
            k = int(counts[i])
            end = start + k
            losses[i] = severities_all[start:end].sum()
            start = end

    if save_csv:
        pd.DataFrame({"loss": losses}).to_csv(RESULTS_PATH, index=False)

    # Summary metrics
    mean = float(np.mean(losses))
    std = float(np.std(losses, ddof=1))
    var95 = float(np.percentile(losses, 95))
    var99 = float(np.percentile(losses, 99))

    # TVaR (a.k.a. Expected Shortfall)
    tvar95 = float(losses[losses >= var95].mean()) if np.any(losses >= var95) else var95
    tvar99 = float(losses[losses >= var99].mean()) if np.any(losses >= var99) else var99

    summary = {
        "sims": int(n_sim),
        "frequency_model": freq_params.get("model"),
        "severity_model": sev_params.get("model"),
        "mean": mean,
        "stdev": std,
        "VaR95": var95,
        "TVaR95": tvar95,
        "VaR99": var99,
        "TVaR99": tvar99,
    }

    print("\n=== Aggregate Loss Summary ===")
    for k, v in summary.items():
        print(f"{k}: {v}")

    return losses, summary


if __name__ == "__main__":
    run_simulation()
