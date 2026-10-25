# =====================================
# PDF
# =====================================

pdf("ex05_r.pdf", width = 8, height = 10)

# Title
plot.new()
title("Exercise 15 Check with R")

mean <- 63.5
sd <- 4.54
n <- 800

# P(62.6 ≤ W ≤ 67.13)
p  <- pnorm(67.13, mean, sd) - pnorm(62.6, mean, sd)
N  <- n * p

# P(W > 68.95)
p2 <- 1 - pnorm(68.95, mean, sd)
N2 <- n * p2


text(0.1, 0.8, sprintf("P(62.6 ≤ W ≤ 67.13) = %.6f", p), cex=1.2, adj=0)
text(0.1, 0.75, sprintf("N = %.2f", N), cex=1.2, adj=0)

text(0.1, 0.65, sprintf("P(W > 68.95) = %.6f", p2), cex=1.2, adj=0)
text(0.1, 0.60, sprintf("N = %.2f", N2), cex=1.2, adj=0)

dev.off()