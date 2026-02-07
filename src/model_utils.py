"""
Utility functions for model persistence and management.
"""
import joblib
import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict
from config import SARIMA_MODEL_FILE, MODEL_METADATA_FILE
from logger import setup_logger, log_success, log_error

logger = setup_logger(__name__)

def save_model(model: Any, metadata: Dict = None) -> bool:
    """
    Save trained model and metadata to disk.
    
    Args:
        model: Trained model object (SARIMAX results)
        metadata: Optional dictionary with model information
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Save model
        joblib.dump(model, SARIMA_MODEL_FILE)
        log_success(logger, f"Model saved to {SARIMA_MODEL_FILE}")
        
        # Save metadata
        if metadata:
            metadata['saved_at'] = datetime.now().isoformat()
            metadata['model_file'] = str(SARIMA_MODEL_FILE)
            
            with open(MODEL_METADATA_FILE, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            log_success(logger, f"Metadata saved to {MODEL_METADATA_FILE}")
        
        return True
    
    except Exception as e:
        log_error(logger, f"Failed to save model: {e}")
        return False

def load_model(check_metadata: bool = True) -> Any:
    """
    Load trained model from disk.
    
    Args:
        check_metadata: Whether to load and display metadata
    
    Returns:
        Loaded model object
    
    Raises:
        FileNotFoundError: If model file doesn't exist
    """
    try:
        if not SARIMA_MODEL_FILE.exists():
            raise FileNotFoundError(
                f"Model file not found: {SARIMA_MODEL_FILE}\n"
                f"Please train the model first using train_sarima.py"
            )
        
        model = joblib.load(SARIMA_MODEL_FILE)
        log_success(logger, f"Model loaded from {SARIMA_MODEL_FILE}")
        
        # Load and display metadata
        if check_metadata and MODEL_METADATA_FILE.exists():
            with open(MODEL_METADATA_FILE, 'r') as f:
                metadata = json.load(f)
            
            logger.info("\n--- Model Metadata ---")
            for key, value in metadata.items():
                logger.info(f"{key}: {value}")
        
        return model
    
    except FileNotFoundError as e:
        log_error(logger, str(e))
        raise
    except Exception as e:
        log_error(logger, f"Failed to load model: {e}")
        raise

def get_model_info() -> Dict:
    """
    Get information about the saved model.
    
    Returns:
        Dictionary with model information
    """
    info = {
        'model_exists': SARIMA_MODEL_FILE.exists(),
        'model_path': str(SARIMA_MODEL_FILE),
        'metadata_exists': MODEL_METADATA_FILE.exists(),
        'metadata_path': str(MODEL_METADATA_FILE)
    }
    
    if SARIMA_MODEL_FILE.exists():
        info['model_size_mb'] = SARIMA_MODEL_FILE.stat().st_size / (1024 * 1024)
        info['model_modified'] = datetime.fromtimestamp(
            SARIMA_MODEL_FILE.stat().st_mtime
        ).isoformat()
    
    if MODEL_METADATA_FILE.exists():
        with open(MODEL_METADATA_FILE, 'r') as f:
            info['metadata'] = json.load(f)
    
    return info
