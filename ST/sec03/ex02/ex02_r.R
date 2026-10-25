# Ex4: Chain length problem with PDF output
# Parameters
n <- 1002  # number of links
mu1 <- 5   # expected value (part 1)
mu2 <- 4.99  # expected value (part 2)
sigma <- 0.2  # standard deviation (sqrt(0.04))

# Start PDF device
pdf("ex4_chain_length_analysis.pdf", width = 10, height = 12)

# Create layout for multiple plots
layout(matrix(c(1, 2, 3, 3), 2, 2, byrow = TRUE), heights = c(1, 1.5))

# Calculate sum statistics
E_S1 <- n * mu1  # Expected value of sum (part 1)
E_S2 <- n * mu2  # Expected value of sum (part 2)
Var_S <- n * sigma^2  # Variance of sum
SD_S <- sqrt(Var_S)  # Standard deviation of sum

# Part 1: P(S <= 5000) when E[X] = 5
z1 <- (5000 - E_S1) / SD_S
prob1 <- pnorm(5000, mean = E_S1, sd = SD_S)

# Part 2: P(S <= 5000) when E[X] = 4.99
z2 <- (5000 - E_S2) / SD_S
prob2 <- pnorm(5000, mean = E_S2, sd = SD_S)

# === Plot 1: Text output for Part 1 ===
par(mar = c(0, 0, 0, 0))
plot.new()
text(0.5, 0.95, "Ex4: Chain Length Problem - Analysis Results", 
     cex = 1.5, font = 2, adj = 0.5)

output1 <- c(
  "=== Part 1: E[X] = 5 ===",
  sprintf("Number of links: n = %d", n),
  sprintf("E[X] = %.2f cm, Var(X) = %.2f", mu1, sigma^2),
  "",
  "Statistics of Sum S = X₁ + X₂ + ... + X₁₀₀₂:",
  sprintf("E[S] = n × E[X] = %d × %.2f = %.2f cm", n, mu1, E_S1),
  sprintf("Var(S) = n × Var(X) = %d × %.2f = %.2f", n, sigma^2, Var_S),
  sprintf("SD(S) = √Var(S) = %.4f cm", SD_S),
  "",
  "Finding P(S ≤ 5000):",
  sprintf("Standardization: z = (5000 - %.2f) / %.4f = %.4f", E_S1, SD_S, z1),
  sprintf("P(S ≤ 5000) = Φ(%.4f) = %.6f ≈ %.4f", z1, prob1, prob1)
)

y_pos <- seq(0.85, 0.05, length.out = length(output1))
for (i in 1:length(output1)) {
  text(0.05, y_pos[i], output1[i], adj = 0, family = "mono", cex = 0.8)
}

# === Plot 2: Text output for Part 2 ===
par(mar = c(0, 0, 0, 0))
plot.new()

output2 <- c(
  "=== Part 2: E[X] = 4.99 ===",
  sprintf("E[X] = %.2f cm, Var(X) = %.2f", mu2, sigma^2),
  "",
  "Statistics of Sum S:",
  sprintf("E[S] = n × E[X] = %d × %.2f = %.2f cm", n, mu2, E_S2),
  sprintf("Var(S) = %.2f (same as Part 1)", Var_S),
  sprintf("SD(S) = %.4f cm", SD_S),
  "",
  "Finding P(S ≤ 5000):",
  sprintf("Standardization: z = (5000 - %.2f) / %.4f = %.4f", E_S2, SD_S, z2),
  sprintf("P(S ≤ 5000) = Φ(%.4f) = %.6f ≈ %.4f", z2, prob2, prob2),
  "",
  "=== Comparison and Interpretation ===",
  sprintf("Difference in E[X]: %.2f - %.2f = %.2f cm per link", mu1, mu2, mu1 - mu2),
  sprintf("Total difference: %d × %.2f = %.2f cm", n, mu1 - mu2, E_S1 - E_S2),
  sprintf("Change in probability: %.4f - %.4f = %.4f", prob2, prob1, prob2 - prob1),
  "",
  "Conclusion: A tiny 0.01 cm difference per link accumulates",
  sprintf("to %.2f cm over 1002 links, dramatically changing the", E_S1 - E_S2),
  "probability from 5.7% to 50.1% - a 44.4 percentage point increase!"
)

y_pos2 <- seq(0.95, 0.05, length.out = length(output2))
for (i in 1:length(output2)) {
  text(0.05, y_pos2[i], output2[i], adj = 0, family = "mono", cex = 0.8)
}

# === Plot 3: Visualization ===
par(mar = c(5, 4, 4, 2) + 0.1)

# Create data for plotting
x <- seq(4900, 5100, length.out = 1000)
y1 <- dnorm(x, mean = E_S1, sd = SD_S)
y2 <- dnorm(x, mean = E_S2, sd = SD_S)

# Plot both distributions
plot(x, y1, type = "l", col = "blue", lwd = 2, 
     xlab = "Total Chain Length (cm)", ylab = "Density",
     main = "Impact of Small Change in Expected Link Length\nDistribution of Total Chain Length (1002 links)",
     ylim = c(0, max(y1, y2) * 1.1))
lines(x, y2, col = "red", lwd = 2)

# Add shaded areas for P(S <= 5000)
x_shade1 <- seq(4900, 5000, length.out = 500)
y_shade1 <- dnorm(x_shade1, mean = E_S1, sd = SD_S)
polygon(c(4900, x_shade1, 5000), c(0, y_shade1, 0), 
        col = rgb(0, 0, 1, 0.3), border = NA)

x_shade2 <- seq(4900, 5000, length.out = 500)
y_shade2 <- dnorm(x_shade2, mean = E_S2, sd = SD_S)
polygon(c(4900, x_shade2, 5000), c(0, y_shade2, 0), 
        col = rgb(1, 0, 0, 0.3), border = NA)

# Add vertical line at 5000
abline(v = 5000, lty = 2, col = "black", lwd = 2)
text(5000, max(y1) * 1.05, "Target: 5000 cm", pos = 4, cex = 0.9)

# Add legend
legend("topleft", 
       legend = c(
         sprintf("E[X] = 5.00: P(S ≤ 5000) = %.4f", prob1),
         sprintf("E[X] = 4.99: P(S ≤ 5000) = %.4f", prob2)
       ),
       col = c("blue", "red"), lwd = 2, bty = "n", cex = 0.9)

# Add mean lines
abline(v = E_S1, col = "blue", lty = 3, lwd = 1.5)
abline(v = E_S2, col = "red", lty = 3, lwd = 1.5)

dev.off()


