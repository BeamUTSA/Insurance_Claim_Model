import os
import json
from datetime import datetime
from data_prep import generate_synthetic_data
from r_bridge import fit_frequency, fit_severity
from plot_results import plot_severity_fit

RESULTS_DIR = "results"

def save_json(data, filename):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    filepath = os.path.join(RESULTS_DIR, filename)

    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
    print(f"[INFO] Saved output to {filepath}")

def run_modeling_pipeline():
    print("=== Running Insurance Loss Model Pipeline ===")

    # Generate synthetic data
    df = generate_synthetic_data(10000)

    # Fit frequency and severity models
    freq_results = fit_frequency()
    sev_results = fit_severity()

    # Save results to JSON
    save_json(freq_results, "frequency_results.json")
    save_json(sev_results, "severity_results.json")

    # Save visualization
    plot_severity_fit(df["ClaimAmount"], sev_results, save=True)

if __name__ == "__main__":
    run_modeling_pipeline()
