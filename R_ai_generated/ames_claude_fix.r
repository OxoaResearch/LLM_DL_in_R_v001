# --- Load data ---
df <- read.csv("../datasets/07_obfuscated/data.csv",
    stringsAsFactors = FALSE
)

# int_as_float: store the target as an integer
df$x81 <- as.integer(round(df$x81))

# Encode every non-numeric column as a single integer column (label encoding).
# High-cardinality categoricals stay as ONE numeric column, not many dummies.
for (col in names(df)) if (!is.numeric(df[[col]])) df[[col]] <- as.numeric(as.factor(df[[col]]))

# Impute missing values with the column median (no rows removed).
for (col in names(df)) df[[col]][is.na(df[[col]])] <- median(df[[col]], na.rm = TRUE)

# --- Same 70/30 split as before ---
set.seed(1)
train_idx <- sample(seq_len(nrow(df)), size = 0.7 * nrow(df))
train <- df[train_idx, ]
test <- df[-train_idx, ]

# R_numeric_scale_imbalance: standardize predictors using TRAIN statistics,
# then apply the same shift/scale to test (no leakage).
pred_cols <- setdiff(names(df), "x81")
mu <- sapply(train[pred_cols], mean)
sdv <- sapply(train[pred_cols], sd)
sdv[sdv == 0] <- 1 # keep constant columns, avoid /0
for (col in pred_cols) {
    train[[col]] <- (train[[col]] - mu[col]) / sdv[col]
    test[[col]] <- (test[[col]] - mu[col]) / sdv[col]
}

# R_imbalanced_target_variable: model the skewed target on the log scale.
# Formula placed directly in the call.
model <- lm(log(x81) ~ ., data = train)

# Predict, back-transform to original scale, compute RMSE on test data.
pred <- exp(predict(model, newdata = test))
rmse <- sqrt(mean((test$x81 - pred)^2))
cat("Test RMSE:", rmse, "\n")
