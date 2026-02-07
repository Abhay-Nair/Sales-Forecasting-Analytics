'''
🧠 What Model Does This Imply?

We now know:

Trend → ✔ handled by differencing

Seasonality → ✔ visible (yearly)

Data frequency → Monthly

✅ Correct Model Choice:

SARIMA (Seasonal ARIMA)


Before coding, we design like engineers.

🧩 SARIMA Parameters Explained (Interview-Ready)

SARIMA = (p, d, q) × (P, D, Q, m)

Non-Seasonal:

d = 1 ✅ (confirmed)

p = autoregressive lags (we’ll start small)

q = moving average lags

Seasonal:

m = 12 → monthly data = yearly seasonality

D = 1 → seasonal differencing (usually needed)

P, Q → seasonal AR & MA

📌 We don’t overfit early.

🎯 Our First (Baseline) SARIMA Model
SARIMA(1,1,1)(1,1,1,12)


Why?

Industry-standard starting point

Stable

Interpretable

Easy to improve later
'''
import pandas as pd
from pathlib import Path
import sys
from statsmodels.tsa.statespace.sarimax import SARIMAX
from config import (
    CLEANED_SALES_FILE,
    SARIMA_ORDER,
    SARIMA_SEASONAL_ORDER,
    ENFORCE_STATIONARITY,
    ENFORCE_INVERTIBILITY
)
from logger import setup_logger, log_section, log_success, log_error
from model_utils import save_model

logger = setup_logger(__name__)

def load_monthly_sales():
    """Load and aggregate sales data to monthly level."""
    try:
        if not CLEANED_SALES_FILE.exists():
            raise FileNotFoundError(
                f"Cleaned data not found: {CLEANED_SALES_FILE}\n"
                f"Please run data_cleaning.py first"
            )
        
        df = pd.read_csv(CLEANED_SALES_FILE, parse_dates=["order_date"])
        monthly_sales = (
            df.set_index("order_date")
              .resample("M")["sales"]
              .sum()
        )
        
        if len(monthly_sales) < 24:
            raise ValueError(f"Insufficient data: only {len(monthly_sales)} months available. Need at least 24 months for SARIMA")
        
        log_success(logger, f"Loaded {len(monthly_sales)} months of sales data")
        return monthly_sales
    
    except FileNotFoundError as e:
        log_error(logger, str(e))
        sys.exit(1)
    except Exception as e:
        log_error(logger, f"Error loading data: {e}")
        sys.exit(1)

def train_sarima(series):
    """Train SARIMA model on sales data."""
    try:
        logger.info(f"\nTraining SARIMA{SARIMA_ORDER}x{SARIMA_SEASONAL_ORDER}...")
        
        model = SARIMAX(
            series,
            order=SARIMA_ORDER,
            seasonal_order=SARIMA_SEASONAL_ORDER,
            enforce_stationarity=ENFORCE_STATIONARITY,
            enforce_invertibility=ENFORCE_INVERTIBILITY
        )
        results = model.fit(disp=False)
        
        log_success(logger, "Model trained successfully")
        return results
    
    except Exception as e:
        log_error(logger, f"Error training model: {e}")
        raise

def main():
    try:
        log_section(logger, "SARIMA MODEL TRAINING")
        
        sales = load_monthly_sales()
        model_results = train_sarima(sales)

        log_section(logger, "MODEL SUMMARY")
        print(model_results.summary())
        
        # Save model with metadata
        metadata = {
            'model_type': 'SARIMA',
            'order': SARIMA_ORDER,
            'seasonal_order': SARIMA_SEASONAL_ORDER,
            'n_observations': len(sales),
            'date_range': f"{sales.index.min()} to {sales.index.max()}",
            'aic': float(model_results.aic),
            'bic': float(model_results.bic)
        }
        
        save_model(model_results, metadata)
        
        log_section(logger, "TRAINING COMPLETED SUCCESSFULLY")
        
    except Exception as e:
        log_error(logger, f"Training failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
