import pytest
from unittest.mock import MagicMock, patch
from PIL import Image
from src.logic.logic_gate import run_mock_inference, run_pipeline, evaluate_logic_gate
from src.logic.state import PipelineStage, InferenceState
from src.logic.exceptions import InferenceError

class MockSessionState(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)
    def __setattr__(self, key, value):
        self[key] = value

@patch("streamlit.session_state", MockSessionState())
def test_run_mock_inference_error_scenario():
    """Verify that run_mock_inference handles the error_scenario correctly."""
    import streamlit as st
    st.session_state.inference = InferenceState()
    
    with pytest.raises(InferenceError) as excinfo:
        for _ in run_mock_inference("error_scenario"):
            pass
    
    assert "Simulated Plane Classification Failure" in str(excinfo.value)
    
    inference = st.session_state.inference
    assert inference.model_status["plane"] == "Error"
    assert any(log["event"] == "ERROR" and "Simulated model timeout" in log["metadata"]["error"] for log in inference.step_logs)

@patch("streamlit.session_state", MockSessionState())
def test_run_mock_inference_status_updates():
    """Verify that run_mock_inference updates model_status on success."""
    import streamlit as st
    st.session_state.inference = InferenceState()
    
    for _ in run_mock_inference("axial_flair"):
        pass
    
    inference = st.session_state.inference
    assert inference.model_status["plane"] == "Complete"
    assert inference.model_status["sequence"] == "Complete"
    assert inference.model_status["depth"] == "Complete"
    assert inference.model_status["narrative"] == "Complete"

@patch("streamlit.session_state", MockSessionState())
def test_evaluate_logic_gate_skipped_status():
    """Verify that evaluate_logic_gate sets status to 'Skipped' when logic gate requirements are not met."""
    state = InferenceState(
        results={"plane": "Sagittal", "sequence": "T1"}
    )
    mock_image = MagicMock(spec=Image.Image)
    
    for _ in evaluate_logic_gate(state, mock_image):
        pass
    
    assert state.model_status["narrative"] == "Skipped"

@patch("streamlit.session_state", MockSessionState())
def test_run_pipeline_plane_error():
    """Verify that run_pipeline handles errors in Plane CNN."""
    import streamlit as st
    st.session_state.inference = InferenceState()
    mock_image = MagicMock(spec=Image.Image)
    
    with patch("src.logic.logic_gate.ModelPlaneCNN") as MockPlane:
        mock_plane_instance = MockPlane.return_value
        mock_plane_instance.predict.side_effect = Exception("GPU out of memory")
        
        with pytest.raises(InferenceError) as excinfo:
            for _ in run_pipeline(mock_image):
                pass
        
        assert "Plane Classification Failed" in str(excinfo.value)
        inference = st.session_state.inference
        assert inference.model_status["plane"] == "Error"
        assert any(log["event"] == "ERROR" and "GPU out of memory" in log["metadata"]["error"] for log in inference.step_logs)
