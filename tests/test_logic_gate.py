from unittest.mock import MagicMock, patch
import pytest
from src.logic.logic_gate import run_mock_inference
from src.logic.state import PipelineStage, InferenceState

class MockSessionState(dict):
    """A dictionary that allows attribute access, similar to st.session_state."""
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"MockSessionState has no attribute {key}")
    def __setattr__(self, key, value):
        self[key] = value

@patch("streamlit.session_state", MockSessionState())
def test_run_mock_inference_success():
    """Test that run_mock_inference correctly populates the session state."""
    # Initialize session state with an InferenceState object
    import streamlit as st
    st.session_state.inference = InferenceState()
    
    run_mock_inference("axial_flair")
    
    inference = st.session_state.inference
    assert inference.is_mock_mode is True
    assert inference.current_stage == PipelineStage.COMPLETE
    assert inference.results["plane"] == "Axial"
    assert inference.results["sequence"] == "FLAIR"
    assert len(inference.step_logs) == 3
    assert "timestamp" in inference.step_logs[0]

@patch("streamlit.session_state", MockSessionState())
def test_run_mock_inference_resets_state():
    """Test that run_mock_inference clears existing state first."""
    import streamlit as st
    st.session_state.inference = InferenceState(
        results={"old": "data"},
        step_logs=[{"old": "log"}]
    )
    
    run_mock_inference("sagittal_t1")
    
    inference = st.session_state.inference
    assert "old" not in inference.results
    assert len(inference.step_logs) == 2  # sagittal_t1 has 2 logs
    assert inference.results["plane"] == "Sagittal"
