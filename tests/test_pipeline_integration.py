from unittest.mock import MagicMock, patch
import pytest
from PIL import Image
from src.logic.logic_gate import run_pipeline
from src.logic.state import PipelineStage, InferenceState
import streamlit as st

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
@patch("src.logic.logic_gate.ModelPlaneCNN")
@patch("src.logic.logic_gate.ModelSeqCNN")
@patch("src.logic.logic_gate.ModelDepthCNN")
@patch("src.logic.logic_gate.ModelMedGemmaVLM")
def test_run_pipeline_full_flow(MockVLM, MockDepth, MockSeq, MockPlane):
    """Test the full pipeline integration and state updates."""
    # Setup mocks
    mock_image = MagicMock(spec=Image.Image)
    
    MockPlane.return_value.predict.return_value = {"label": "axial", "confidence": 0.9, "raw_scores": [0.1, 0.9]}
    MockSeq.return_value.predict.return_value = {"label": "flair", "confidence": 0.8, "raw_scores": [0.2, 0.8]}
    MockDepth.return_value.predict.return_value = {"label": "slice_10", "confidence": 0.7, "raw_scores": [0.3, 0.7]}
    MockVLM.return_value.predict.return_value = {"text": "Patient has a brain."}
    
    # Initialize session state
    st.session_state.inference = InferenceState()
    
    # Run pipeline
    for _ in run_pipeline(mock_image):
        pass
    
    inference = st.session_state.inference
    
    # Verify stages
    assert inference.current_stage == PipelineStage.COMPLETE
    
    # Verify results
    assert inference.results["plane"] == "axial"
    assert inference.results["sequence"] == "flair"
    assert inference.results["depth"] == "slice_10"
    assert inference.results["narrative"] == "Patient has a brain."
    assert inference.results["confidence"] == pytest.approx(0.8) # (0.9 + 0.8 + 0.7) / 3
    
    # Verify logs
    log_events = [log["event"] for log in inference.step_logs]
    assert "PLANE_CLASSIFIED" in log_events
    assert "SEQUENCE_CLASSIFIED" in log_events
    assert "DEPTH_ESTIMATED" in log_events
    assert "GATE_DECISION" in log_events
    
    # Verify timestamps
    for log in inference.step_logs:
        assert "timestamp" in log
        # Simple ISO format check (very basic)
        assert "T" in log["timestamp"]
