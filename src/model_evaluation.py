import pandas as pd
import numpy as np
from pathlib import Path
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
from config import (
    CLEANED_SALES_FILE,
    TEST_SIZE,
    SARIMA_ORDER,
    SARIMA_SEASONAL_ORDER,
    ENFORCE_STATIONARITY,
    ENFORCE_INVERTIBILITY,
    FIGURE_SIZE
)
from visualization import plot_model_evaluation

# ----------------------------
# Load cleaned data
# ----------------------------
df = pd.read_csv(CLEANED_SALES_FILE, parse_dates=["order_date"])

# Aggregate to monthly sales
monthly_sales = (
    df.set_index("order_date")
      .resample("M")["sales"]
      .sum()
)

# ----------------------------
# Train-test split (last 12 months as test)
# ----------------------------
train = monthly_sales[:-TEST_SIZE]
test = monthly_sales[-TEST_SIZE:]

print("Train period:", train.index.min(), "to", train.index.max())
print("Test period :", test.index.min(), "to", test.index.max())

# ----------------------------
# Fit SARIMA on TRAIN data
# ----------------------------
model = SARIMAX(
    train,
    order=SARIMA_ORDER,
    seasonal_order=SARIMA_SEASONAL_ORDER,
    enforce_stationarity=ENFORCE_STATIONARITY,
    enforce_invertibility=ENFORCE_INVERTIBILITY
)

results = model.fit(disp=False)

# ----------------------------
# Predict on TEST period
# ----------------------------
predictions = results.predict(
    start=test.index[0],
    end=test.index[-1],
    typ="levels"
)

# ----------------------------
# Evaluation metrics
# ----------------------------
mae = mean_absolute_error(test, predictions)
rmse = np.sqrt(mean_squared_error(test, predictions))
mape = np.mean(np.abs((test - predictions) / test)) * 100

print("\n--- Model Evaluation ---")
print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"MAPE : {mape:.2f}%")

# ----------------------------
# Plot: Train vs Test vs Prediction
# ----------------------------
metrics = {'mae': mae, 'rmse': rmse, 'mape': mape}
plot_model_evaluation(train, test, predictions, metrics, save=True)
