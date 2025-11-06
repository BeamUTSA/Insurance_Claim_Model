"""
Bridge between Python and R using rpy2.
Provides functions that load and execute R scripts, then return model parameters.
"""
import os

from rpy2 import robjects
from rpy2.rinterface import NULL
from rpy2.robjects import NA_Logical, NA_Integer, NA_Real, NA_Character

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def run_r_script(relative_path: str):
    full_path = os.path.join(PROJECT_ROOT, relative_path)
    full_path = full_path.replace("\\", "/")
    print(f"\n[DEBUG] Loading R script at: {full_path}")

    # Try sourcing and catch R errors explicitly:
    try:
        robjects.r(f'source("{full_path}")')
        print(f"[DEBUG] Successfully sourced: {relative_path}")
    except Exception as e:
        print(f"[ERROR] Failed to source: {relative_path}")
        print(f"[DETAILS] {e}")
        raise

def get_r_list(name: str) -> dict:
    """Converts an R list object into a Python dictionary."""
    r_obj = robjects.globalenv[name]
    return {key: _convert_r_value(r_obj.rx2(key)) for key in r_obj.names}

def _convert_r_value(value):
    # Handle NULL or empty
    if value is NULL:
        return None
    if len(value) == 0:
        return None

    # Handle R NA types
    first_val = value[0]
    if first_val in (NA_Logical, NA_Integer, NA_Real, NA_Character):
        return None

    # Try numeric
    try:
        return float(first_val)
    except Exception:
        pass

    # Try string
    try:
        return str(first_val)
    except Exception:
        pass

    # Fallback to list
    try:
        return list(value)
    except Exception:
        return value

def fit_frequency():
    """Runs frequency_model.R and returns Python dict of params."""
    run_r_script("r/frequency_model.R")
    return get_r_list("frequency_params")

def fit_severity():
    """Runs severity_model.R and returns Python dict of params."""
    run_r_script("r/severity_model.R")
    return get_r_list("severity_params")