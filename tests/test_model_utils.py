"""
Unit tests for model utilities module.
"""
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from model_utils import get_model_info

class TestModelInfo:
    """Tests for model information retrieval."""
    
    def test_get_model_info_structure(self):
        """Test that get_model_info returns expected structure."""
        info = get_model_info()
        
        # Check required keys
        assert "model_exists" in info
        assert "model_path" in info
        assert "metadata_exists" in info
        assert "metadata_path" in info
        
        # Check types
        assert isinstance(info["model_exists"], bool)
        assert isinstance(info["model_path"], str)
        assert isinstance(info["metadata_exists"], bool)
        assert isinstance(info["metadata_path"], str)
    
    def test_model_path_format(self):
        """Test that model path ends with correct filename."""
        info = get_model_info()
        assert info["model_path"].endswith("sarima_model.pkl")
    
    def test_metadata_path_format(self):
        """Test that metadata path ends with correct filename."""
        info = get_model_info()
        assert info["metadata_path"].endswith("model_metadata.json")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
