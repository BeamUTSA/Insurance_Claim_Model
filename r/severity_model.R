library(fitdistrplus)
library(actuar)

# Simulate large sample of claim sizes (severity data)
set.seed(123)
claim_sizes <- rgamma(50000, shape = 2, rate = 0.001)  # Mean = 2000

# Check data variability
if (length(unique(claim_sizes)) > 1) {

  # Attempt to fit Gamma using MME (more robust than MLE)
  gamma_fit <- tryCatch(
  {
    fitdist(claim_sizes, "gamma", method = "mme")  # Moment matching
  },
    error = function() NULL
  )

  # Attempt Lognormal fit
  lognorm_fit <- tryCatch(
  {
    fitdist(claim_sizes, "lnorm")  # Default MLE works reliably here
  },
    error = function() NULL
  )

  # Prepare output based on success of fits
  severity_params <- list(
    model = "both",
    gamma_shape = if (!is.null(gamma_fit)) gamma_fit$estimate["shape"] else NA,
    gamma_rate  = if (!is.null(gamma_fit)) gamma_fit$estimate["rate"] else NA,
    ln_meanlog  = if (!is.null(lognorm_fit)) lognorm_fit$estimate["meanlog"] else NA,
    ln_sdlog    = if (!is.null(lognorm_fit)) lognorm_fit$estimate["sdlog"] else NA,
    aic_gamma   = if (!is.null(gamma_fit)) gamma_fit$aic else NA,
    aic_lognorm = if (!is.null(lognorm_fit)) lognorm_fit$aic else NA
  )
} else {
  # Fallback if data has no variance
  severity_params <- list(
    model = "none",
    gamma_shape = NA, gamma_rate = NA, ln_meanlog = NA,
    ln_sdlog = NA, aic_gamma = NA, aic_lognorm = NA
  )
}
