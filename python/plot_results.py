import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gamma, lognorm

def plot_severity_fit(claims, params, save=False):
    x = np.linspace(0, claims.max(), 200)
    fig, ax = plt.subplots(figsize=(10, 5))

    # Plot empirical data
    ax.hist(claims, bins=100, density=True, alpha=0.5, label="Empirical Data")

    # Plot Gamma fit
    if params.get('gamma_shape') and params.get('gamma_rate'):
        g_shape, g_rate = params['gamma_shape'], params['gamma_rate']
        ax.plot(x, gamma.pdf(x, g_shape, scale=1/g_rate), label="Gamma Fit")

    # Plot Log-normal fit
    if params.get('ln_meanlog') and params.get('ln_sdlog'):
        s, scale = params['ln_sdlog'], np.exp(params['ln_meanlog'])
        ax.plot(x, lognorm.pdf(x, s, scale=scale), label="Log-Normal Fit")

    ax.legend()
    ax.set_title("Severity Model Fit")
    ax.set_xlabel("Claim Size")
    ax.set_ylabel("Density")

    if save:
        os.makedirs("results/figs", exist_ok=True)
        fig.savefig("results/figs/severity_fit.png", dpi=300)
        print("[INFO] Saved plot to results/figs/severity_fit.png")

    plt.close(fig)  # avoid showing when running automated pipelines
