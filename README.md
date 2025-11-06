# Insurance Claim Model

This project explores the integration of **R actuarial models** into a **Python-based workflow** using the `rpy2` package. It was developed to support academic study in **Statistics and Data Science**, with a focus on **actuarial science and risk analysis**.

The repository showcases the use of both **frequency** and **severity models** for insurance claims. It demonstrates importing and executing R scripts from Python, exposing model parameters and enabling further statistical analysis, visualization, and automation in Python-based systems.

---

## Project Structure

```file
Insurance_Claim_Model/
│
├── python/ # Python bridge logic and test runner
│ ├── r_bridge.py # Python <-> R interface logic
│ └── test_script.py # Main entry point for running models
│
├── r/ # R model scripts
│ ├── frequency_model.R # Poisson GLM for claim frequency
│ ├── severity_model.R # Gamma and Lognormal model for claim severity
│ └── util.R # Helper functions for data and R utilities
│
├── data/ # Sample input datasets
├── results/ # Output directory for model results
└── README.md # Project description
```

---

## Models Implemented

### 1. Frequency Model (Poisson GLM)
A Generalized Linear Model is applied to predict claim counts based on:

- Vehicle Power  
- Vehicle Age  
- Driver Age  
- Bonus-Malus Rating  

Output parameters (returned to Python):
- Model type  
- Mean claim rate (mu)  
- AIC for model comparison  

### 2. Severity Model
Fits two standard distribution models to claim sizes:

- Gamma Distribution  
- Lognormal Distribution  

Output parameters:
- Gamma shape and rate  
- Lognormal mean and standard deviation (on the log scale)  
- AIC values for both distributions  
- Identifies the better model

---

## How to Run

### Prerequisites
- Python 3.10+ with `rpy2` installed  
- R (>= 4.0) with packages: `actuar`, `fitdistrplus`, `MASS`  
- Windows users should ensure Rtools is installed if building from source

### Run in Python

From the root of the project:
```shell
python python/test_script.py
```
Results will be printed in the terminal and optionally saved to /results.

### Concept and Academic Focus

The purpose of this project is to:

- Demonstrate statistical modeling workflows common in actuarial science  
- Bridge R’s robust actuarial/statistical packages with Python automation  
- Support academic coursework in:
  - Statistics  
  - Data Science  
  - Actuarial Methods (with specialist focus)

---

### Future Work

- Build end-to-end pipelines for claim prediction  
- Expand severity and frequency model options  
- Add simulation-based reserve studies  
- Develop visualizations to display model comparisons  

---

### License

This project is for academic and learning use only.  
No financial or actuarial advice is implied.
