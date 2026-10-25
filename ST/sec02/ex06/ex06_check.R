# =====================================
# PDF Output
# =====================================

pdf("ex06_r.pdf", width = 8, height = 10)

# Set up empty plot
plot.new()

# Main Title
mtext("R Probability Tutorials", side = 3, line = 2, cex = 1.5)

# ----------------------------
# Tutorial 17: Poisson Example
# ----------------------------

lambda <- 0.6

# 1. Exact probability P(X = 2)
p_exact2 <- dpois(2, lambda)
text(0.1, 0.8, sprintf("Tutorial 17: P(X = 2) = %.6f", p_exact2), cex = 1.2, adj = 0)

# 2. Probability P(X >= 2)
p_2ormore <- 1 - (dpois(0, lambda) + dpois(1, lambda))
text(0.1, 0.75, sprintf("P(X >= 2) = %.6f", p_2ormore), cex = 1.2, adj = 0)

# ----------------------------
# Tutorial 19: Multinomial Example
# ----------------------------

p <- c(R = 0.5, G = 0.3, B = 0.2)
x <- c(R = 2, G = 1, B = 2)
prob <- dmultinom(x, prob = p)
text(0.1, 0.65, sprintf("Tutorial 19: P(X) = %.4f", prob), cex = 1.2, adj = 0)

# ----------------------------
# Tutorial 20: Geometric / Binomial Example
# ----------------------------

p <- 0.6

# 2. Probability of at least 4 wins before first loss (geometric)
P_at_least4 <- 1 - pgeom(3-1, prob = p)  # 3 wins before first loss
text(0.1, 0.55, sprintf("Tutorial 20: P(at least 4 wins) = %.4f", P_at_least4), cex = 1.2, adj = 0)

# 3. Probability of winning tournament in 6 rounds (binomial)
rounds <- 6
P_tournament_win <- p^rounds
text(0.1, 0.50, sprintf("P(Tournament win in 6 rounds) = %.4f", P_tournament_win), cex = 1.2, adj = 0)

# Close PDF
dev.off()
