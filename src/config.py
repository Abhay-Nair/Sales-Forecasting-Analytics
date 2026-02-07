"""
Configuration file for Sales Forecasting Project
Centralizes all paths, constants, and parameters
"""
from pathlib import Path

# ============================================
# PROJECT PATHS
# ============================================
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
RESULTS_DIR = PROJECT_ROOT / "results"
MODELS_DIR = PROJECT_ROOT / "models"

# Ensure directories exist
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# ============================================
# DATA FILES
# ============================================
RAW_SALES_FILE = RAW_DATA_DIR / "superstore_sales.csv"
CLEANED_SALES_FILE = PROCESSED_DATA_DIR / "superstore_sales_cleaned.csv"
FORECAST_OUTPUT_FILE = PROCESSED_DATA_DIR / "sales_forecast_12_months.csv"

# ============================================
# MODEL FILES
# ============================================
SARIMA_MODEL_FILE = MODELS_DIR / "sarima_model.pkl"
MODEL_METADATA_FILE = MODELS_DIR / "model_metadata.json"

# ============================================
# FORECASTING PARAMETERS
# ============================================
FORECAST_HORIZON = 12  # months
TEST_SIZE = 12  # months for validation

# ============================================
# SARIMA MODEL PARAMETERS
# ============================================
SARIMA_ORDER = (1, 1, 1)  # (p, d, q)
SARIMA_SEASONAL_ORDER = (1, 1, 1, 12)  # (P, D, Q, m)
ENFORCE_STATIONARITY = False
ENFORCE_INVERTIBILITY = False

# ============================================
# DATA CLEANING PARAMETERS
# ============================================
NUMERIC_COLUMNS = ["sales", "profit", "shipping_cost"]
DATE_COLUMNS = ["order_date", "ship_date"]
DUPLICATE_SUBSET = ["order_id", "product_id"]

# ============================================
# VISUALIZATION SETTINGS
# ============================================
FIGURE_SIZE = (12, 6)
PLOT_DPI = 100
PLOT_STYLE = "seaborn-v0_8-darkgrid"  # matplotlib style

# ============================================
# LOGGING CONFIGURATION
# ============================================
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "sales_forecasting.log"
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
