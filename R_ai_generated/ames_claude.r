# Load data
df <- read.csv("../datasets/07_obfuscated/data.csv"
,
    stringsAsFactors = FALSE
)

# Explicitly convert every non-numeric column to numeric (label encoding)
for (col in names(df)) if (!is.numeric(df[[col]])) df[[col]] <- as.numeric(as.factor(df[[col]]))

# Median-impute remaining NAs so no rows are silently dropped
for (col in names(df)) df[[col]][is.na(df[[col]])] <- median(df[[col]], na.rm = TRUE)

# 70/30 train-test split
set.seed(1)
train_idx <- sample(seq_len(nrow(df)), size = 0.7 * nrow(df))
train <- df[train_idx, ]
test <- df[-train_idx, ]

# Fit OLS regression (formula placed directly in the call)
model <- lm(x81 ~ ., data = train)

# Predict and compute RMSE on the test set
pred <- predict(model, newdata = test)
rmse <- sqrt(mean((test$x81 - pred)^2))
cat("Test RMSE:", rmse, "\n")
