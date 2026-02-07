"""
Visualization Utilities for Sales Forecasting Project

Centralized plotting functions with consistent styling.
"""
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from config import FIGURE_SIZE, RESULTS_DIR
from logger import setup_logger, log_success

logger = setup_logger(__name__)

def save_plot(filename: str, dpi: int = 300):
    """
    Save current plot to results directory.
    
    Args:
        filename: Name of the file (e.g., 'forecast.png')
        dpi: Resolution in dots per inch
    
    Returns:
        Path to saved file
    """
    filepath = RESULTS_DIR / filename
    plt.savefig(filepath, dpi=dpi, bbox_inches='tight')
    plt.close()
    log_success(logger, f"Plot saved to {filepath}")
    return filepath

def plot_monthly_sales(monthly_sales: pd.DataFrame, save: bool = True):
    """
    Plot monthly sales trend with improved styling.
    
    Args:
        monthly_sales: DataFrame with order_date and sales columns
        save: Whether to save the plot to file
    
    Returns:
        Path to saved file if save=True, None otherwise
    """
    plt.figure(figsize=FIGURE_SIZE)
    plt.plot(monthly_sales["order_date"], monthly_sales["sales"], 
             linewidth=2, color='#2E86AB', marker='o', markersize=4)
    
    plt.title("Monthly Sales Trend", fontsize=16, fontweight='bold', pad=20)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Total Sales ($)", fontsize=12)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    # Add summary statistics
    avg_sales = monthly_sales["sales"].mean()
    plt.axhline(y=avg_sales, color='red', linestyle='--', 
                label=f'Average: ${avg_sales:,.0f}', alpha=0.7)
    plt.legend()
    
    if save:
        return save_plot("monthly_sales_trend.png")
    else:
        plt.show()
        return None

def plot_forecast(sales: pd.Series, forecast: pd.Series, 
                  conf_int: pd.DataFrame, save: bool = True):
    """
    Plot actual sales with forecast and confidence intervals.
    
    Args:
        sales: Historical sales data
        forecast: Forecasted sales
        conf_int: Confidence intervals DataFrame
        save: Whether to save the plot to file
    
    Returns:
        Path to saved file if save=True, None otherwise
    """
    plt.figure(figsize=FIGURE_SIZE)
    
    # Plot actual sales
    plt.plot(sales.index, sales.values, 
             label="Actual Sales", linewidth=2, color='#2E86AB')
    
    # Plot forecast
    plt.plot(forecast.index, forecast.values, 
             label="Forecast", linewidth=2, color='#E63946', linestyle='--')
    
    # Plot confidence interval
    plt.fill_between(
        conf_int.index,
        conf_int.iloc[:, 0],
        conf_int.iloc[:, 1],
        color='#E63946',
        alpha=0.2,
        label="95% Confidence Interval"
    )
    
    # Styling
    plt.title(f"Sales Forecast ({len(forecast)} Months)", 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Sales ($)", fontsize=12)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    # Add vertical line separating actual from forecast
    plt.axvline(x=sales.index[-1], color='gray', linestyle=':', alpha=0.5)
    
    if save:
        return save_plot("forecast_plot.png")
    else:
        plt.show()
        return None

def plot_model_evaluation(train: pd.Series, test: pd.Series, 
                          predictions: pd.Series, metrics: dict, save: bool = True):
    """
    Plot train/test split with predictions and metrics.
    
    Args:
        train: Training data
        test: Test data
        predictions: Model predictions on test set
        metrics: Dictionary with MAE, RMSE, MAPE
        save: Whether to save the plot to file
    
    Returns:
        Path to saved file if save=True, None otherwise
    """
    plt.figure(figsize=FIGURE_SIZE)
    
    # Plot data
    plt.plot(train.index, train.values, 
             label="Train", linewidth=2, color='#2E86AB')
    plt.plot(test.index, test.values, 
             label="Actual (Test)", linewidth=2, color='#06A77D')
    plt.plot(predictions.index, predictions.values, 
             label="Predicted", linewidth=2, color='#E63946', linestyle='--')
    
    # Add metrics text box
    metrics_text = f"MAE: ${metrics['mae']:,.2f}\nRMSE: ${metrics['rmse']:,.2f}\nMAPE: {metrics['mape']:.2f}%"
    plt.text(0.02, 0.98, metrics_text, 
             transform=plt.gca().transAxes,
             fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Styling
    plt.title("SARIMA Model Validation", fontsize=16, fontweight='bold', pad=20)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Sales ($)", fontsize=12)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    # Add vertical line separating train from test
    plt.axvline(x=train.index[-1], color='gray', linestyle=':', alpha=0.5)
    
    if save:
        return save_plot("model_evaluation.png")
    else:
        plt.show()
        return None
