from unittest.mock import MagicMock, patch
import pytest
from PIL import Image
from src.logic.logic_gate import run_mock_inference, evaluate_logic_gate
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

def test_evaluate_logic_gate_triggered():
    """Test that VLM is triggered for Axial-FLAIR scans."""
    state = InferenceState(
        results={"plane": "Axial", "sequence": "FLAIR"}
    )
    mock_image = MagicMock(spec=Image.Image)
    
    with patch("src.logic.logic_gate.ModelMedGemmaVLM") as MockVLM:
        mock_vlm_instance = MockVLM.return_value
        mock_vlm_instance.predict.return_value = {"label": "Narrative", "text": "Clinical findings..."}
        
        evaluate_logic_gate(state, mock_image)
        
        # Verify VLM was called
        MockVLM.assert_called_once()
        mock_vlm_instance.predict.assert_called_once_with(mock_image)
        
        # Verify results
        assert state.results["narrative"] == "Clinical findings..."
        
        # Verify logging
        assert any(log["event"] == "GATE_DECISION" and log["outcome"] == "TRIGGERED" for log in state.step_logs)

def test_evaluate_logic_gate_skipped():
    """Test that VLM is skipped for non Axial-FLAIR scans."""
    state = InferenceState(
        results={"plane": "Sagittal", "sequence": "T1"}
    )
    mock_image = MagicMock(spec=Image.Image)
    
    with patch("src.logic.logic_gate.ModelMedGemmaVLM") as MockVLM:
        evaluate_logic_gate(state, mock_image)
        
        # Verify VLM was NOT called
        MockVLM.assert_not_called()
        
        # Verify results
        assert state.results["narrative"] == "Analysis Skipped (Scan not Axial-FLAIR)"
        
        # Verify logging
        assert any(log["event"] == "GATE_DECISION" and log["outcome"] == "SKIPPED" for log in state.step_logs)

