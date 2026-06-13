import pytest
from src.logic.state import InferenceState

def test_inference_state_model_status_default():
    """Verify that model_status is initialized with default empty dict."""
    state = InferenceState()
    assert hasattr(state, "model_status")
    assert state.model_status == {
        "plane": "Pending",
        "sequence": "Pending",
        "depth": "Pending",
        "narrative": "Pending"
    }

def test_inference_state_model_status_update():
    """Verify that model_status can be updated correctly."""
    state = InferenceState()
    state.model_status["plane"] = "Processing"
    assert state.model_status["plane"] == "Processing"
    
    state.model_status["plane"] = "Complete"
    assert state.model_status["plane"] == "Complete"
    
    state.model_status["narrative"] = "Error"
    assert state.model_status["narrative"] == "Error"

def test_inference_state_model_status_skipped():
    """Verify that model_status handles 'Skipped' state."""
    state = InferenceState()
    state.model_status["narrative"] = "Skipped"
    assert state.model_status["narrative"] == "Skipped"
