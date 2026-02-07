'''“We used SARIMA because the data exhibited both trend and yearly seasonality.
After differencing to ensure stationarity, the model produced stable forecasts with well-behaved residuals.
The widening confidence intervals reflect increasing uncertainty, which is expected in long-horizon forecasting.”'''

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
from statsmodels.tsa.statespace.sarimax import SARIMAX
from config import (
    CLEANED_SALES_FILE,
    FORECAST_OUTPUT_FILE,
    FORECAST_HORIZON,
    SARIMA_ORDER,
    SARIMA_SEASONAL_ORDER,
    ENFORCE_STATIONARITY,
    ENFORCE_INVERTIBILITY,
    FIGURE_SIZE
)
from logger import setup_logger, log_section, log_success, log_error
from model_utils import load_model, get_model_info
from visualization import plot_forecast

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
        
        log_success(logger, f"Loaded {len(monthly_sales)} months of sales data")
        return monthly_sales
    
    except Exception as e:
        log_error(logger, f"Error loading data: {e}")
        sys.exit(1)

def train_model(series):
    """Train SARIMA model (fallback if no saved model exists)."""
    logger.info(f"\nTraining new SARIMA{SARIMA_ORDER}x{SARIMA_SEASONAL_ORDER} model...")
    model = SARIMAX(
        series,
        order=SARIMA_ORDER,
        seasonal_order=SARIMA_SEASONAL_ORDER,
        enforce_stationarity=ENFORCE_STATIONARITY,
        enforce_invertibility=ENFORCE_INVERTIBILITY
    )
    return model.fit(disp=False)

def forecast_next(model, steps=None):
    if steps is None:
        steps = FORECAST_HORIZON
    forecast = model.get_forecast(steps=steps)
    return forecast.predicted_mean, forecast.conf_int()

def main():
    try:
        log_section(logger, "SALES FORECASTING")
        
        # Try to load saved model first
        model_info = get_model_info()
        
        if model_info['model_exists']:
            logger.info("\n✓ Found saved model, loading...")
            model = load_model(check_metadata=True)
        else:
            logger.info("\n⚠ No saved model found, training new model...")
            sales = load_monthly_sales()
            model = train_model(sales)
            log_success(logger, "Model trained successfully")
        
        # Load sales data for plotting
        sales = load_monthly_sales()
        
        # Generate forecast
        logger.info(f"\nGenerating {FORECAST_HORIZON}-month forecast...")
        forecast, conf_int = forecast_next(model)
        log_success(logger, "Forecast generated successfully")

        # Plot and save
        plot_forecast(sales, forecast, conf_int, save=True)

        # Save forecast
        forecast_df = forecast.reset_index()
        forecast_df.columns = ["date", "forecast_sales"]
        forecast_df.to_csv(FORECAST_OUTPUT_FILE, index=False)
        log_success(logger, f"Forecast saved to {FORECAST_OUTPUT_FILE}")
        
        # Display forecast summary
        logger.info("\n--- Forecast Summary ---")
        logger.info(f"Forecast period: {forecast.index.min()} to {forecast.index.max()}")
        logger.info(f"Average forecasted sales: ${forecast.mean():,.2f}")
        logger.info(f"Min forecasted sales: ${forecast.min():,.2f}")
        logger.info(f"Max forecasted sales: ${forecast.max():,.2f}")
        
        log_section(logger, "FORECASTING COMPLETED")
        
    except Exception as e:
        log_error(logger, f"Forecasting failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
