# ==========================================
# frequency_model.R
# Fits frequency model using simulated vehicle and claim count data
# ==========================================

suppressMessages(library(MASS))

# Simulated data
set.seed(123)
n <- 10000
VehPower <- sample(50:250, n, replace = TRUE)
VehAge <- sample(1:15, n, replace = TRUE)
DrivAge <- sample(18:75, n, replace = TRUE)
BonusMalus <- sample(1:150, n, replace = TRUE)
ClaimNb <- rpois(n, lambda = 0.07 * (VehPower / 150) * (BonusMalus / 100))

freq_data <- data.frame(VehPower, VehAge, DrivAge, BonusMalus, ClaimNb)

# Fit frequency models
pois_model <- glm(
  ClaimNb ~ VehPower + VehAge + DrivAge + BonusMalus,
  family = poisson,
  data = freq_data
)

# Check overdispersion
dispersion <- sum(residuals(pois_model, type = "pearson")^2) / pois_model$df.residual
if (dispersion > 1.5) {
  freq_model <- glm.nb(
    ClaimNb ~ VehPower + VehAge + DrivAge + BonusMalus,
    data = freq_data
  )
  model_type <- "NegBin"
  theta <- freq_model$theta
} else {
  freq_model <- pois_model
  model_type <- "Poisson"
  theta <- NA
}

frequency_params <- list(
  model = model_type,
  mu = mean(freq_data$ClaimNb),
  theta = theta,
  aic = AIC(freq_model)
)

if (interactive()) {
  print(summary(freq_model))
  print(frequency_params)
}
