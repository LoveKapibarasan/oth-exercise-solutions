# Set CRAN mirror
options(repos = c(CRAN = "https://cran.rstudio.com/"))

# Install gridExtra
install.packages("gridExtra")
library(gridExtra)

##################


# Create PDF
pdf("ex02_r.pdf", width = 8.27, height = 11.69)
##################



plot.new()
plot.window(xlim = c(0, 1), ylim = c(0, 1))
text(0.5, 0.5, "Exercise 4", cex = 3, font = 2)

# Data
data <- c(1, 2, 2, 3, 4, 5, 7, 8, 9, 9)
n <- length(data)

# 1. Sample mean
mean_x <- mean(data)

# 2. Variance and standard deviation
variance_s2 <- var(data)  # Sample variance
sd_s <- sd(data)          # Sample standard deviation

# 3. Median, 5-number summary, range, and IQR
median_M <- median(data)

# 5-number summary [L, Q1, M, Q3, H]
five_num <- fivenum(data)
L <- five_num[1]   # Minimum
Q1 <- five_num[2]  # First quartile
M <- five_num[3]   # Median
Q3 <- five_num[4]  # Third quartile
H <- five_num[5]   # Maximum

# Range
range_val <- H - L

# Interquartile range (IQR)
IQR_val <- IQR(data)  # or Q3 - Q1


# Page 2: Results
par(mfrow = c(1, 1), mar = c(1, 1, 1, 1))
plot.new()
plot.window(xlim = c(0, 1), ylim = c(0, 1))

text(0.5, 0.95, "Results", cex = 1.5, font = 2)

y_pos <- 0.85
text(0.5, y_pos, paste("1. Mean (x̄) =", round(mean_x, 2)), cex = 1.2)

y_pos <- y_pos - 0.1
text(0.5, y_pos, paste("2. Variance (s²) =", round(variance_s2, 2)), cex = 1.2)
y_pos <- y_pos - 0.05
text(0.5, y_pos, paste("   Standard deviation (s) =", round(sd_s, 2)), cex = 1.2)

y_pos <- y_pos - 0.1
text(0.5, y_pos, paste("3. Median (M) =", median_M), cex = 1.2)
y_pos <- y_pos - 0.05
text(0.5, y_pos, paste("   5-number summary = [", L, ",", Q1, ",", M, ",", Q3, ",", H, "]"), cex = 1.1)
y_pos <- y_pos - 0.05
text(0.5, y_pos, paste("   Range =", range_val), cex = 1.2)
y_pos <- y_pos - 0.05
text(0.5, y_pos, paste("   IQR =", IQR_val), cex = 1.2)


###########################
plot.new()
plot.window(xlim = c(0, 1), ylim = c(0, 1))
text(0.5, 0.5, "Exercise 5", cex = 3, font = 2)
# Placeholder data (n = 30 children ages)
data <- c(2, 3, 4, 1, 2, 2, 3, 4, 4, 3,
          2, 2, 6, 2, 4, 1, 2, 6, 4, 2,
          2, 3, 7, 1, 2, 3, 2, 4, 2, 6)

n <- length(data)

# 1. Frequency distribution
freq_table <- table(data)
f <- as.vector(freq_table)
x <- as.numeric(names(freq_table))
F <- cumsum(f)

distribution <- data.frame(
  Age_x = x,
  Frequency_f = f,
  Cumulative_F = F
)

###
plot.new()
grid.table(distribution)

# 2. Sample mean, variance, and standard deviation
mean_x <- mean(data)
variance_s2 <- var(data)
sd_s <- sd(data)


# 3. Median, 5-number summary, range, and IQR
median_M <- median(data)

# 5-number summary [L, Q1, M, Q3, H]
five_num <- fivenum(data)
L <- five_num[1]   # Minimum
Q1 <- five_num[2]  # First quartile
M <- five_num[3]   # Median
Q3 <- five_num[4]  # Third quartile
H <- five_num[5]   # Maximum

# Range
range_val <- H - L

# Interquartile range (IQR)
IQR_val <- IQR(data)



# Page: Results
par(mfrow = c(1, 1), mar = c(1, 1, 1, 1))
plot.new()
plot.window(xlim = c(0, 1), ylim = c(0, 1))

text(0.5, 0.95, "Statistical Summary", cex = 1.5, font = 2)

y_pos <- 0.85
text(0.5, y_pos, "2. Measures of Center and Spread", cex = 1.2, font = 2)
y_pos <- y_pos - 0.05
text(0.5, y_pos, paste("Mean (x̄) =", round(mean_x, 2)), cex = 1.1)
y_pos <- y_pos - 0.04
text(0.5, y_pos, paste("Variance (s²) =", round(variance_s2, 2)), cex = 1.1)
y_pos <- y_pos - 0.04
text(0.5, y_pos, paste("Standard deviation (s) =", round(sd_s, 2)), cex = 1.1)

y_pos <- y_pos - 0.08
text(0.5, y_pos, "3. Five-Number Summary", cex = 1.2, font = 2)
y_pos <- y_pos - 0.05
text(0.5, y_pos, paste("Median (M) =", median_M), cex = 1.1)
y_pos <- y_pos - 0.04
text(0.5, y_pos, paste("5-number summary = [", L, ",", Q1, ",", M, ",", Q3, ",", H, "]"), cex = 1.1)
y_pos <- y_pos - 0.04
text(0.5, y_pos, paste("Range =", range_val), cex = 1.1)
y_pos <- y_pos - 0.04
text(0.5, y_pos, paste("IQR =", IQR_val), cex = 1.1)


###########################
plot.new()
plot.window(xlim = c(0, 1), ylim = c(0, 1))
text(0.5, 0.5, "Exercise 6", cex = 3, font = 2)
# Placeholder data (n = 18)
data <- c(2, 7, 4, 1, 6, 4, 8, 15, 12,
          7, 3, 16, 1, 2, 11, 5, 15, 4)

n <- length(data)

# 1. Sample mean
mean_x <- mean(data)

# 2. Median, 5-number summary, range, and IQR
median_M <- median(data)

# 5-number summary [L, Q1, M, Q3, H]
five_num <- fivenum(data)
L <- five_num[1]   # Minimum
Q1 <- five_num[2]  # First quartile
M <- five_num[3]   # Median
Q3 <- five_num[4]  # Third quartile
H <- five_num[5]   # Maximum

# Range
range_val <- H - L

# IQR
IQR_val <- IQR(data)

# Results page
par(mfrow = c(1, 1), mar = c(1, 1, 1, 1))
plot.new()
plot.window(xlim = c(0, 1), ylim = c(0, 1))

text(0.5, 0.9, "Results", cex = 1.5, font = 2)

y_pos <- 0.75
text(0.5, y_pos, paste("1. Sample mean (x̄) =", round(mean_x, 2)), cex = 1.2)

y_pos <- y_pos - 0.1
text(0.5, y_pos, "2. Five-Number Summary and Spread", cex = 1.2, font = 2)
y_pos <- y_pos - 0.06
text(0.5, y_pos, paste("Median (M) =", median_M), cex = 1.1)
y_pos <- y_pos - 0.05
text(0.5, y_pos, paste("5-number summary [L, Q1, M, Q3, H] = [", L, ",", Q1, ",", M, ",", Q3, ",", H, "]"), cex = 1.1)
y_pos <- y_pos - 0.05
text(0.5, y_pos, paste("Range =", range_val), cex = 1.1)
y_pos <- y_pos - 0.05
text(0.5, y_pos, paste("IQR =", IQR_val), cex = 1.1)


###########################


# Title page
plot.new()
plot.window(xlim = c(0, 1), ylim = c(0, 1))
text(0.5, 0.5, "Tutorial 2", cex = 3, font = 2)

# Placeholder frequency distribution
x <- c(1:6)
f <- c(2, 4, 6, 8, 3, 2)

# Expand data (repeat each x by its frequency)
data <- rep(x, f)
n <- length(data)

# 1. Sample mean, variance, and standard deviation
mean_x <- mean(data)
variance_s2 <- var(data)
sd_s <- sd(data)



# 2. Median, quartiles, 5-number summary, range, and IQR
median_M <- median(data)
Q1 <- quantile(data, 0.25)
Q3 <- quantile(data, 0.75)

# 5-number summary
five_num <- fivenum(data)
L <- five_num[1]
Q1_five <- five_num[2]
M <- five_num[3]
Q3_five <- five_num[4]
H <- five_num[5]

# Range and IQR
range_val <- H - L
IQR_val <- IQR(data)

# Results page
par(mfrow = c(1, 1), mar = c(1, 1, 1, 1))
plot.new()
plot.window(xlim = c(0, 1), ylim = c(0, 1))

text(0.5, 0.95, "Results", cex = 1.5, font = 2)

y_pos <- 0.85
text(0.5, y_pos, "1. Measures of Center and Spread", cex = 1.2, font = 2)
y_pos <- y_pos - 0.05
text(0.5, y_pos, paste("Sample mean (x̄) =", round(mean_x, 2)), cex = 1.1)
y_pos <- y_pos - 0.04
text(0.5, y_pos, paste("Variance (s²) =", round(variance_s2, 2)), cex = 1.1)
y_pos <- y_pos - 0.04
text(0.5, y_pos, paste("Standard deviation (s) =", round(sd_s, 2)), cex = 1.1)

y_pos <- y_pos - 0.08
text(0.5, y_pos, "2. Five-Number Summary", cex = 1.2, font = 2)
y_pos <- y_pos - 0.05
text(0.5, y_pos, paste("Median (M) =", median_M), cex = 1.1)
y_pos <- y_pos - 0.04
text(0.5, y_pos, paste("Q1 =", Q1), cex = 1.1)
y_pos <- y_pos - 0.04
text(0.5, y_pos, paste("Q3 =", Q3), cex = 1.1)
y_pos <- y_pos - 0.04
text(0.5, y_pos, paste("5-number summary [L, Q1, M, Q3, H] = [", L, ",", Q1_five, ",", M, ",", Q3_five, ",", H, "]"), cex = 1.1)
y_pos <- y_pos - 0.04
text(0.5, y_pos, paste("Range =", range_val), cex = 1.1)
y_pos <- y_pos - 0.04
text(0.5, y_pos, paste("IQR =", IQR_val), cex = 1.1)

##########################
plot.new()
plot.window(xlim = c(0, 1), ylim = c(0, 1))
text(0.5, 0.5, "Exercise 7", cex = 3, font = 2)

# Data from OCR
data <- c(31, 53, 57, 58, 63, 66, 67, 67, 67, 68, 69, 70,
          70, 70, 70, 72, 73, 75, 75, 76, 76, 78, 79, 81)

# 1. Median and quartiles
median_M <- median(data)
Q1 <- quantile(data, 0.25)
Q3 <- quantile(data, 0.75)

# 2. Boxplot statistics
five_num <- fivenum(data)
L <- five_num[1]
H <- five_num[5]
IQR_val <- IQR(data)

# Check for outliers
# Outlier if: x < Q1 - 1.5*IQR  or  x > Q3 + 1.5*IQR
lower_fence <- Q1 - 1.5 * IQR_val
upper_fence <- Q3 + 1.5 * IQR_val


# 3. Comment on value 31
cat("3. Comment on value 31:\n")
if (31 > upper_fence) {
  cat("   31 is an OUTLIER (31 >", upper_fence, ")\n")
  cat("   It is unusually high compared to the other data points.\n")
} else if (31 < lower_fence) {
  cat("   31 is an OUTLIER (31 <", lower_fence, ")\n")
  cat("   It is unusually low compared to the other data points.\n")
} else {
  cat("   31 is NOT an outlier.\n")
  cat("   It falls within the normal range of the data.\n")
}

# Page 1: Boxplot
par(mfrow = c(1, 1), mar = c(5, 5, 4, 2))
boxplot(data, horizontal = TRUE, col = "lightblue",
        main = "Boxplot",
        xlab = "Data Value")
grid()

# Page 2: Results
par(mfrow = c(1, 1), mar = c(1, 1, 1, 1))
plot.new()
plot.window(xlim = c(0, 1), ylim = c(0, 1))

text(0.5, 0.95, "Results", cex = 1.5, font = 2)

y_pos <- 0.85
text(0.5, y_pos, "1. Median and Quartiles", cex = 1.2, font = 2)
y_pos <- y_pos - 0.05
text(0.5, y_pos, paste("Median (M) =", median_M), cex = 1.1)
y_pos <- y_pos - 0.04
text(0.5, y_pos, paste("Lower quartile (Q1) =", Q1), cex = 1.1)
y_pos <- y_pos - 0.04
text(0.5, y_pos, paste("Upper quartile (Q3) =", Q3), cex = 1.1)

y_pos <- y_pos - 0.08
text(0.5, y_pos, "2. Boxplot Statistics", cex = 1.2, font = 2)
y_pos <- y_pos - 0.05
text(0.5, y_pos, paste("IQR =", IQR_val), cex = 1.1)
y_pos <- y_pos - 0.04
text(0.5, y_pos, paste("Lower fence =", round(lower_fence, 2)), cex = 1.1)
y_pos <- y_pos - 0.04
text(0.5, y_pos, paste("Upper fence =", round(upper_fence, 2)), cex = 1.1)

y_pos <- y_pos - 0.08
text(0.5, y_pos, "3. Comment on value 31", cex = 1.2, font = 2)
y_pos <- y_pos - 0.05
if (31 > upper_fence) {
  text(0.5, y_pos, paste("31 is an OUTLIER (31 >", round(upper_fence, 2), ")"), cex = 1.1, col = "red")
  y_pos <- y_pos - 0.04
  text(0.5, y_pos, "It is unusually high compared to the other data points.", cex = 1.1)
} else if (31 < lower_fence) {
  text(0.5, y_pos, paste("31 is an OUTLIER (31 <", round(lower_fence, 2), ")"), cex = 1.1, col = "red")
  y_pos <- y_pos - 0.04
  text(0.5, y_pos, "It is unusually low compared to the other data points.", cex = 1.1)
} else {
  text(0.5, y_pos, "31 is NOT an outlier (statistically).", cex = 1.1, col = "darkgreen")
  y_pos <- y_pos - 0.04
  text(0.5, y_pos, "However, it is noticeably separated from the rest of the data.", cex = 1.1)
}


###########################
dev.off()
