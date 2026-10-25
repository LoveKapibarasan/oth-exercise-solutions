# =====================================
# PDF
# =====================================

# Open PDF
pdf("ex04_r.pdf", width = 8, height = 10)

# par(mfrow = c(2, 1))

# Tutorial 10
n1 <- 3 
p1 <- 0.5  
prob_3heads <- dbinom(3, size = n1, prob = p1)
prob_2heads <- dbinom(2, size = n1, prob = p1)
prob_1head  <- dbinom(1, size = n1, prob = p1)
prob_0heads <- dbinom(0, size = n1, prob = p1)

plot.new()
plot.window(xlim = c(0, 1), ylim = c(0, 5))

text(0.5, 5, "Tutorial 10", cex = 1.5, font = 2)

text(0.1, 4, paste0("1. 3 heads: ", prob_3heads), adj = 0)
text(0.1, 3, paste0("2. exactly 2 heads,: ", prob_2heads), adj = 0)
text(0.1, 2, paste0("3. exactly 1 head,: ", prob_1head), adj = 0)
text(0.1, 1, paste0("4. no heads: ", prob_0heads), adj = 0)
barplot(dbinom(0:3, size = n1, prob = p1),
        names.arg = 0:3,
        main = "Tutorial 10",
        xlab = "the number of heads",
        ylab = "P(X = x)",
        col = "lightblue")

# Tutorial 11
n2 <- 6   
p2 <- 1/4
prob_exactly_2 <- dbinom(2, size = n2, prob = p2)
prob_more_than_4 <- dbinom(5, size = n2, prob = p2) + dbinom(6, size = n2, prob = p2)
prob_at_least_1 <- 1 - dbinom(0, size = n2, prob = p2)
cat("3. : ", prob_at_least_1, "\n")

plot.new()
plot.window(xlim = c(0, 1), ylim = c(0, 5))

text(0.5, 5, "Tutorial 11", cex = 1.5, font = 2)

text(0.1, 4, paste0("1. exactly 2 times, : ", prob_exactly_2), adj = 0)
text(0.1, 3, paste0("2. more than 4 times,: ", prob_more_than_4), adj = 0)
text(0.1, 2, paste0("3. at least 1 time: ", prob_at_least_1), adj = 0)

barplot(dbinom(0:6, size = n2, prob = p2),
        names.arg = 0:6,
        main = "Tutorial 11",
        xlab = "the number of hits",
        ylab = "P(X=x)",
        col = "lightgreen")

# Tutorial 12
n3 <- 4   
p3 <- 0.2  # 20% defective
prob_2_defective <- dbinom(2, size = n3, prob = p3)
prob_3_defective <- dbinom(3, size = n3, prob = p3)
prob_0_defective <- dbinom(0, size = n3, prob = p3)

plot.new()
plot.window(xlim = c(0, 1), ylim = c(0, 5))

text(0.5, 5, "Tutorial 12", cex = 1.5, font = 2)

text(0.1, 4, paste0("1. 2 defective: ", prob_2_defective), adj = 0)
text(0.1, 3, paste0("2. 3 defective: ", prob_3_defective), adj = 0)
text(0.1, 2, paste0("3. 0 defective: ", prob_0_defective), adj = 0)

barplot(dbinom(0:4, size = n3, prob = p3),
        names.arg = 0:4,
        main = "Tutorial 12",
        xlab = "Number of defective items",
        ylab = "P(X = x)",
        col = "lightcoral")

# Tutorial 13
n4 <- 8   
p4 <- 0.5  # Equal probability for male/female
expected_girls <- n4 * p4  # Expected number of girls
prob_expected_girls <- dbinom(expected_girls, size = n4, prob = p4)

plot.new()
plot.window(xlim = c(0, 1), ylim = c(0, 5))

text(0.5, 5, "Tutorial 13", cex = 1.5, font = 2)

text(0.1, 4, paste0("1. Expected girls: ", expected_girls), adj = 0)
text(0.1, 3, paste0("2. P(exactly ", expected_girls, " girls): ", prob_expected_girls), adj = 0)

barplot(dbinom(0:8, size = n4, prob = p4),
        names.arg = 0:8,
        main = "Tutorial 13",
        xlab = "Number of girls",
        ylab = "P(X = x)",
        col = "lightyellow")

# Tutorial 14
n5 <- 100
p5 <- 1/10  # 10% chance of hitting the target
expected_hits <- n5 * p5
std_dev_hits <- sqrt(n5 * p5 * (1 - p5))

plot.new()
plot.window(xlim = c(0, 1), ylim = c(0, 5))

text(0.5, 5, "Tutorial 14", cex = 1.5, font = 2)

text(0.1, 4, paste0("1. Expected hits: ", expected_hits), adj = 0)
text(0.1, 3, paste0("2. Std. dev. of hits: ", std_dev_hits), adj = 0)

barplot(dbinom(0:n5, size = n5, prob = p5),
        names.arg = 0:n5,
        main = "Tutorial 14",
        xlab = "Number of hits",
        ylab = "P(X = x)",
        col = "lightgreen")

# Tutorial 15
n6 <- 10000
p6 <- 0.02  # 2% defective
expected_defective <- n6 * p6
std_dev_defective <- sqrt(n6 * p6 * (1 - p6))

plot.new()
plot.window(xlim = c(0, 1), ylim = c(0, 5))    
text(0.5, 5, "Tutorial 15", cex = 1.5, font = 2)
text(0.1, 4, paste0("1. Expected defective: ", expected_defective), adj = 0)
text(0.1, 3, paste0("2. Std. dev. of defective: ", std_dev_defective), adj = 0)

barplot(dbinom(0:n6, size = n6, prob = p6),
        names.arg = 0:n6,
        main = "Tutorial 15",
        xlab = "Number of defective items",
        ylab = "P(X = x)",
        col = "lightblue")

# Close PDF
dev.off()

