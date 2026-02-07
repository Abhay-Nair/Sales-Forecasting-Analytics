"""
SARIMA Hyperparameter Tuning

This module explores different SARIMA parameter combinations
to find the optimal model based on AIC/BIC criteria.

Usage:
    python src/hyperparameter_tuning.py
"""
import pandas as pd
import numpy as np
from itertools import product
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings
warnings.filterwarnings('ignore')

from config import CLEANED_SALES_FILE, SARIMA_ORDER, SARIMA_SEASONAL_ORDER
from logger import setup_logger, log_section, log_success, log_warning

logger = setup_logger(__name__)

def load_monthly_sales():
    """Load and aggregate sales data to monthly level."""
    df = pd.read_csv(CLEANED_SALES_FILE, parse_dates=["order_date"])
    monthly_sales = (
        df.set_index("order_date")
          .resample("M")["sales"]
          .sum()
    )
    log_success(logger, f"Loaded {len(monthly_sales)} months of sales data")
    return monthly_sales

def grid_search_sarima(series, p_range=(0, 2), d_range=(0, 2), q_range=(0, 2),
                       P_range=(0, 2), D_range=(0, 2), Q_range=(0, 2), m=12):
    """
    Perform grid search over SARIMA parameters.
    
    Args:
        series: Time series data
        p_range: Range for AR order (p)
        d_range: Range for differencing order (d)
        q_range: Range for MA order (q)
        P_range: Range for seasonal AR order (P)
        D_range: Range for seasonal differencing order (D)
        Q_range: Range for seasonal MA order (Q)
        m: Seasonal period (12 for monthly data)
    
    Returns:
        DataFrame with results sorted by AIC
    """
    results = []
    
    # Generate all combinations
    p_values = range(p_range[0], p_range[1] + 1)
    d_values = range(d_range[0], d_range[1] + 1)
    q_values = range(q_range[0], q_range[1] + 1)
    P_values = range(P_range[0], P_range[1] + 1)
    D_values = range(D_range[0], D_range[1] + 1)
    Q_values = range(Q_range[0], Q_range[1] + 1)
    
    total_combinations = (
        len(list(p_values)) * len(list(d_values)) * len(list(q_values)) *
        len(list(P_values)) * len(list(D_values)) * len(list(Q_values))
    )
    
    logger.info(f"\nTesting {total_combinations} parameter combinations...")
    logger.info("This may take a few minutes...\n")
    
    count = 0
    for p, d, q, P, D, Q in product(p_values, d_values, q_values, 
                                      P_values, D_values, Q_values):
        try:
            count += 1
            if count % 10 == 0:
                logger.info(f"Progress: {count}/{total_combinations}")
            
            model = SARIMAX(
                series,
                order=(p, d, q),
                seasonal_order=(P, D, Q, m),
                enforce_stationarity=False,
                enforce_invertibility=False
            )
            
            fitted = model.fit(disp=False, maxiter=50)
            
            results.append({
                'p': p, 'd': d, 'q': q,
                'P': P, 'D': D, 'Q': Q,
                'AIC': fitted.aic,
                'BIC': fitted.bic,
                'order': (p, d, q),
                'seasonal_order': (P, D, Q, m)
            })
            
        except Exception as e:
            # Skip combinations that don't converge
            continue
    
    # Convert to DataFrame and sort by AIC
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('AIC').reset_index(drop=True)
    
    log_success(logger, f"Successfully fitted {len(results_df)} models")
    return results_df

def main():
    try:
        log_section(logger, "SARIMA HYPERPARAMETER TUNING")
        
        # Load data
        sales = load_monthly_sales()
        
        # Current model parameters
        logger.info(f"\nCurrent model: SARIMA{SARIMA_ORDER}x{SARIMA_SEASONAL_ORDER}")
        
        # Perform grid search (limited range for speed)
        logger.info("\nPerforming grid search...")
        logger.info("Parameter ranges:")
        logger.info("  p, q: 0-2")
        logger.info("  d: 0-2")
        logger.info("  P, Q: 0-2")
        logger.info("  D: 0-2")
        logger.info("  m: 12 (fixed)")
        
        results = grid_search_sarima(
            sales,
            p_range=(0, 2), d_range=(0, 2), q_range=(0, 2),
            P_range=(0, 2), D_range=(0, 2), Q_range=(0, 2)
        )
        
        # Display top 10 models
        log_section(logger, "TOP 10 MODELS BY AIC")
        logger.info("\n" + results.head(10).to_string(index=False))
        
        # Highlight current model
        current_model = results[
            (results['p'] == SARIMA_ORDER[0]) &
            (results['d'] == SARIMA_ORDER[1]) &
            (results['q'] == SARIMA_ORDER[2]) &
            (results['P'] == SARIMA_SEASONAL_ORDER[0]) &
            (results['D'] == SARIMA_SEASONAL_ORDER[1]) &
            (results['Q'] == SARIMA_SEASONAL_ORDER[2])
        ]
        
        if not current_model.empty:
            rank = current_model.index[0] + 1
            logger.info(f"\n\nCurrent model rank: #{rank} out of {len(results)}")
            logger.info(f"Current model AIC: {current_model['AIC'].values[0]:.2f}")
            logger.info(f"Best model AIC: {results['AIC'].iloc[0]:.2f}")
            
            improvement = current_model['AIC'].values[0] - results['AIC'].iloc[0]
            if improvement > 2:
                log_warning(logger, f"Potential improvement: {improvement:.2f} AIC points")
                logger.info(f"\nRecommended model: SARIMA{results['order'].iloc[0]}x{results['seasonal_order'].iloc[0]}")
            else:
                log_success(logger, "Current model is near-optimal!")
        
        # Save results
        from config import RESULTS_DIR
        results_file = RESULTS_DIR / "hyperparameter_tuning_results.csv"
        results.to_csv(results_file, index=False)
        log_success(logger, f"Results saved to {results_file}")
        
        log_section(logger, "TUNING COMPLETED")
        
    except Exception as e:
        logger.error(f"Tuning failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
