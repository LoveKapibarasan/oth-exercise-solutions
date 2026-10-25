# Set CRAN mirror
options(repos = c(CRAN = "https://cran.rstudio.com/"))

# Install gridExtra
install.packages("gridExtra")
library(gridExtra)

##################
# Create PDF with plots and text answers
pdf("ex01_r.pdf", width = 11, height = 8.5)


# Exercise 1 Title Page
plot.new()
plot.window(xlim = c(0, 1), ylim = c(0, 1))
text(0.5, 0.5, "Exercise 1", cex = 3, font = 2)

# Placeholder data for the frequency distribution

cat("!! 11 is missing !!\n")
x <- c(9:10, 12:20) # Number of correct answers
f <- c(1,2,1,2,7,2,1,7,2,6,4)    # Number of students

# Create data frame
data <- data.frame(x = x, f = f)

# Calculate mean(Average)
mean_x <- sum(x * f) / sum(f)

# Calculate median
# Create expanded data (each score repeated by its frequency)
expanded_data <- rep(x, f)
median_x <- median(expanded_data)

# Calculate total number of students
n <- sum(f)



# Page 1: Histogram and Frequency Polygon
par(mfrow = c(1, 2), mar = c(5, 5, 4, 2))

# 1. Histogram (using barplot for discrete data)
barplot(f, names.arg = x,
        col = "lightblue",
        border = "black",
        main = "Histogram",
        xlab = "Number of Correct Answers (x)",
        ylab = "Frequency (f)",
        ylim = c(0, max(f) * 1.1))
grid(nx = NA, ny = NULL)

# 2. Frequency Polygon
plot(x, f, type = "b",
     col = "blue",
     pch = 16,
     lwd = 2,
     main = "Frequency Polygon",
     xlab = "Number of Correct Answers (x)",
     ylab = "Frequency (f)",
     ylim = c(0, max(f) * 1.1))
grid()

# Add mean and median lines
abline(v = mean_x, col = "red", lwd = 2, lty = 2)
abline(v = median_x, col = "darkgreen", lwd = 2, lty = 3)
legend("topright",
       legend = c(paste("Mean =", round(mean_x, 2)),
                  paste("Median =", median_x)),
       col = c("red", "darkgreen"),
       lty = c(2, 3),
       lwd = 2,
       cex = 0.8)

# Page 2: Summary Statistics using text()
par(mfrow = c(1, 1), mar = c(1, 1, 1, 1))
plot.new()
plot.window(xlim = c(0, 1), ylim = c(0, 1))

text(0.5, 0.8, "2. ", cex = 2, font = 2)

text(0.5, 0.6, paste("Mean (x̄) =", round(mean_x, 2)), cex = 1.5, col = "red")

text(0.5, 0.4, paste("Median (x̃) =", median_x), cex = 1.5, col = "darkgreen")

cat("Finished 1\n")
###################################

plot.new()
plot.window(xlim = c(0, 1), ylim = c(0, 1))
text(0.5, 0.5, "Exercise 2", cex = 3, font = 2)

# Placeholder data (n = 20)
data <- c(3, 5, 3, 4, 4, 7, 6, 5, 2, 4,
 2, 5, 5, 6, 4, 3, 5, 4, 4, 5)

# 1. Construct frequency distribution (f) and cumulative distribution (F)
freq_table <- table(data)
f <- as.vector(freq_table)
x <- as.numeric(names(freq_table))
F <- cumsum(f)

# Create distribution table
distribution <- data.frame(
  x = x,
  f = f,
  F = F
)

# 2. Calculate mean and median
mean_x <- mean(data)
median_x <- median(data)

# Page 1: Histogram
par(mfrow = c(1, 1), mar = c(5, 5, 4, 2))
barplot(f, names.arg = x,
        col = "lightblue",
        border = "black",
        main = "Histogram",
        xlab = "Data Value (x)",
        ylab = "Frequency (f)",
        ylim = c(0, max(f) * 1.1))
grid(nx = NA, ny = NULL)

# Distribution table
par(mfrow = c(1, 2), mar = c(5, 5, 4, 2))

# Page 2: Distribution table using gridExtra
plot.new()
grid.table(distribution)

# Results
par(mfrow = c(1, 1), mar = c(1, 1, 1, 1))
plot.new()
plot.window(xlim = c(0, 1), ylim = c(0, 1))

text(0.5, 0.7, "Results", cex = 1.5, font = 2)
text(0.5, 0.5, paste("Mean (x̄) =", round(mean_x, 2)), cex = 1.3, col = "red")
text(0.5, 0.3, paste("Median (x̃) =", median_x), cex = 1.3, col = "darkgreen")

cat("Finished 2\n")
#################################

plot.new()
plot.window(xlim = c(0, 1), ylim = c(0, 1))
text(0.5, 0.5, "Exercise 3", cex = 3, font = 2)

# Placeholder data (n = 20 scores)
scores <- c(74, 80, 65, 85, 95, 72, 76, 72, 93, 84,
            75, 77, 60, 74, 75, 63, 78, 87, 90, 70)

# Define class intervals
# Note: If a number falls on a class boundary, it is assigned to the higher class
# So: (60,70], (70,80], (80,90], (90,100]
breaks <- c(60, 70, 80, 90, 100)
class_labels <- c("60-70", "70-80", "80-90", "90-100")


# Cut data into classes (right = TRUE means intervals like (60,70])
classes <- cut(scores, breaks = breaks, right = TRUE, include.lowest = FALSE)

cat("DEBUG: cut result:\n")
print(table(classes))
cat("\n")

# Do not exclude null class
#classes <- factor(classes, levels = class_labels)

cat("DEBUG: after factor:\n")
print(table(classes))
cat("\n")


# Frequency distribution
f <- as.vector(table(classes))
cat("DEBUG f is ", f)
cat("\n")

# Class midpoints
midpoints <- (breaks[-length(breaks)] + breaks[-1]) / 2

# Cumulative distribution
F <- cumsum(f)

# Create frequency table
freq_table <- data.frame(
  Class = class_labels,
  Midpoint_mi = midpoints,
  Frequency_f = f,
  Cumulative_F = F
)

### 1.

# Page 1: Histogram
par(mfrow = c(1, 1), mar = c(5, 5, 4, 2))
barplot(f, names.arg = class_labels,
        col = "lightblue",
        border = "black",
        main = "Histogram (Grouped Data)",
        xlab = "Score Class",
        ylab = "Frequency (f)",
        ylim = c(0, max(f) * 1.1))
grid(nx = NA, ny = NULL)


# Page 2: Frequency Table
plot.new()
par(mfrow = c(1, 1))
grid.table(freq_table)

# Class Value: Middle Point
# Calculate mean using midpoints(class value * freq)
mean_x <- sum(midpoints * f) / sum(f)

# Calculate median
# x̃ = Lc + α·Wc where α = (m - CF_{i-1}) / f_i
# m 中央値の位置
# CF_{i-1}中央値クラスより前の累積度数

n <- sum(f)

# Step 1: Calculate m (median position)
if (n %% 2 == 1) {
  m <- (n + 1) / 2  # n is odd
} else {
  m <- n / 2        # n is even
}

# Step 2: Find the median class
cum_freq <- cumsum(f)
median_class_index <- which(cum_freq >= m)[1]

# Step 3: Linear interpolation
if (median_class_index > 1) {
  Lc <- breaks[median_class_index]                      # Lower boundary
  Uc <- breaks[median_class_index + 1]                  # Upper boundary
  Wc <- Uc - Lc                                         # Class width
  CF_prev <- cum_freq[median_class_index - 1]           # CF_{i-1}
  fi <- f[median_class_index]                           # Frequency of median class

  alpha <- (m - CF_prev) / fi
  median_x <- Lc + alpha * Wc

} else { # if median is in the first class,  cum_freq[0] is 0
  Lc <- breaks[1]
  Wc <- breaks[2] - breaks[1]
  fi <- f[1]

  alpha <- m / fi
  median_x <- Lc + alpha * Wc
}


par(mfrow = c(1, 1), mar = c(1, 1, 1, 1))
plot.new()
plot.window(xlim = c(0, 1), ylim = c(0, 1))

text(0.5, 0.6, paste("Mean (x̄) =", round(mean_x, 2)), cex = 1.5, col = "red")
text(0.5, 0.4, paste("Median (x̃) =", round(median_x, 2)), cex = 1.5, col = "darkgreen")


cat("finished 3\n")
#######################

plot.new()
plot.window(xlim = c(0, 1), ylim = c(0, 1))
text(0.5, 0.5, "Tutorial 1", cex = 3, font = 2)

# Placeholder data (n = 30 yearly rainfall in cm)
rainfall <- c(42.3, 35.7, 47.5, 31.2, 28.3, 37.0, 41.3, 32.4, 41.3, 29.3,
              34.3, 35.2, 43.0, 36.3, 35.7, 41.5, 43.2, 30.7, 38.4, 46.5,
              43.2, 31.7, 43.6, 45.2, 45.2, 32.8, 30.7, 36.2, 34.7, 35.3)

# Define class intervals
# 10 classes: 28-30, 30-32, 32-34, ..., 46-48
breaks <- seq(28, 48, by = 2)  # 28, 30, 32, 34, ..., 46, 48
class_labels <- c("28-30", "30-32", "32-34", "34-36", "36-38",
                  "38-40", "40-42", "42-44", "44-46", "46-48")

# Cut data into classes (right = TRUE means boundary goes to higher class)
classes <- cut(rainfall, breaks = breaks, right = TRUE, include.lowest = FALSE)
#classes <- factor(classes, levels = class_labels)

# Frequency distribution
f <- as.vector(table(classes))

# Class midpoints (mi)
midpoints <- (breaks[-length(breaks)] + breaks[-1]) / 2

# Cumulative distribution (F)
F <- cumsum(f)

# Create frequency table
freq_table <- data.frame(
  Class = class_labels,
  Midpoint_mi = midpoints,
  Frequency_f = f,
  Cumulative_F = F
)



# Calculate mean using midpoints
mean_x <- sum(midpoints * f) / sum(f)

# Calculate median
n <- sum(f)

# Step 1: Calculate m (median position)
if (n %% 2 == 1) {
  m <- (n + 1) / 2  # n is odd
} else {
  m <- n / 2        # n is even
}

# Step 2: Find the median class
cum_freq <- cumsum(f)
median_class_index <- which(cum_freq >= m)[1]

# Step 3: Linear interpolation
# x̃ = Lc + α·Wc where α = (m - CF_{i-1}) / f_i
if (median_class_index > 1) {
  Lc <- breaks[median_class_index]                      # Lower boundary
  Uc <- breaks[median_class_index + 1]                  # Upper boundary
  Wc <- Uc - Lc                                         # Class width
  CF_prev <- cum_freq[median_class_index - 1]           # CF_{i-1}
  fi <- f[median_class_index]                           # Frequency of median class

  alpha <- (m - CF_prev) / fi
  median_x <- Lc + alpha * Wc

} else {
  Lc <- breaks[1]
  Wc <- breaks[2] - breaks[1]
  fi <- f[1]

  alpha <- m / fi
  median_x <- Lc + alpha * Wc
}


# Page 1: Histogram
par(mfrow = c(1, 1), mar = c(5, 5, 4, 2))
barplot(f, names.arg = class_labels,
        col = "lightblue",
        border = "black",
        main = "Histogram - Yearly Rainfall",
        xlab = "Rainfall Class (cm)",
        ylab = "Frequency (f)",
        ylim = c(0, max(f) * 1.1))
grid(nx = NA, ny = NULL)

# Page 2: Frequency Table
plot.new()
library(gridExtra)
grid.table(freq_table)

# Page 3: Results
par(mfrow = c(1, 1), mar = c(1, 1, 1, 1))
plot.new()
plot.window(xlim = c(0, 1), ylim = c(0, 1))

text(0.5, 0.6, paste("Mean (x̄) =", round(mean_x, 2), "cm"), cex = 1.5, col = "red")
text(0.5, 0.4, paste("Median (M) =", round(median_x, 2), "cm"), cex = 1.5, col = "darkgreen")

cat("finished 4\n")

#######################
dev.off()