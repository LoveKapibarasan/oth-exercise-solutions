n <- 4
p <- 0.5
x <- 0:4
prob <- dbinom(x, n, p)

barplot(prob,
        names.arg = x,
        main = "Binomial Distribution (n=4, p=0.5)",
        xlab = "Number of Heads (X)",
        ylab = "P(X)",
        col = "blue",
        ylim = c(0, 0.4))
