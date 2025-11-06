import pandas as pd
import numpy as np

def generate_synthetic_data(n=10000, seed=42):
    np.random.seed(seed)
    data = pd.DataFrame({
        "VehPower": np.random.randint(50, 250, n),
        "VehAge": np.random.randint(0, 20, n),
        "DrivAge": np.random.randint(18, 80, n),
        "BonusMalus": np.random.randint(50, 150, n),
        "ClaimNb": np.random.poisson(0.05, n),  # Avg 0.05 claims per year
        "ClaimAmount": np.random.exponential(2000, n)  # Avg severity = $2000
    })
    return data

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Simple example: remove negative or null values
    return df.dropna().loc[(df >= 0).all(axis=1)]
