from r_bridge import fit_frequency, fit_severity, robjects
import os

print("Current working dir:", os.getcwd())
print("\nR version in use:\n", robjects.r("R.version.string"))
print("\nR library paths:\n", robjects.r(".libPaths()"))

print("=== TEST START ===")
print("Working directory:", os.getcwd())

print("\n>>> Calling fit_frequency()")
freq = fit_frequency()
print("Result:", freq)

print("\n>>> Calling fit_severity()")
sev = fit_severity()
print("Result:", sev)

print("\n=== TEST END ===")

