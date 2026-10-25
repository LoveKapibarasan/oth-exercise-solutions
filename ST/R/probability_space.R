# ========== Definition of Probability Space ==========

# 1. Definition of Sample Space (Ω)
sample_space <- c("outcome1", "outcome2", "outcome3")

# 2. Definition of σ-algebra (F)
# Family of subsets of the sample space
sigma_algebra <- list(
  c(),                           # empty set
  sample_space,                  # whole set
  c("outcome1"),
  c("outcome2"),
  c("outcome3"),
  c("outcome1", "outcome2"),
  c("outcome1", "outcome3"),
  c("outcome2", "outcome3")
)

# 3. Definition of Probability Measure (P)
probability_measure <- c(0.2, 0.3, 0.5)  # probability of each outcome

# Combine probability space into a list
probability_space <- list(
  Omega = sample_space,
  F = sigma_algebra,
  P = probability_measure
)

# Verification
print(probability_space)

save(probability_space, file = "prob_space.RData")
