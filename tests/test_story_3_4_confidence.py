from unittest.mock import MagicMock, patch
import pytest
import streamlit as st
from src.logic.logic_gate import run_mock_inference, run_pipeline
from src.logic.state import InferenceState, PipelineStage
from PIL import Image

class MockSessionState(dict):
    def __getattr__(self, key):
        return self.get(key)
    def __setattr__(self, key, value):
        self[key] = value

@patch("streamlit.session_state", MockSessionState())
def test_mock_inference_includes_individual_confidences():
    """Verify that run_mock_inference populates individual confidence scores."""
    st.session_state.inference = InferenceState()
    
    # Execute the generator to completion
    for _ in run_mock_inference("axial_flair"):
        pass
        
    results = st.session_state.inference.results
    assert "plane_conf" in results
    assert "sequence_conf" in results
    assert "depth_conf" in results
    assert isinstance(results["plane_conf"], float)
    assert isinstance(results["sequence_conf"], float)
    assert isinstance(results["depth_conf"], float)

@patch("streamlit.session_state", MockSessionState())
def test_real_pipeline_includes_individual_confidences():
    """Verify that run_pipeline populates individual confidence scores."""
    st.session_state.inference = InferenceState()
    mock_image = Image.new("RGB", (224, 224))
    
    # Mock all models to return consistent labels and confidences
    with patch("src.logic.logic_gate.ModelPlaneCNN") as M1, \
         patch("src.logic.logic_gate.ModelSeqCNN") as M2, \
         patch("src.logic.logic_gate.ModelDepthCNN") as M3, \
         patch("src.logic.logic_gate.ModelMedGemmaVLM") as M4:
        
        M1.return_value.predict.return_value = {"label": "Axial", "confidence": 0.9}
        M2.return_value.predict.return_value = {"label": "FLAIR", "confidence": 0.8}
        M3.return_value.predict.return_value = {"label": "0.45", "confidence": 0.7}
        M4.return_value.predict.return_value = {"text": "Narrative", "confidence": 0.95}
        
        # Execute generator
        for _ in run_pipeline(mock_image):
            pass
            
        results = st.session_state.inference.results
        assert results["plane_conf"] == 0.9
        assert results["sequence_conf"] == 0.8
        assert results["depth_conf"] == 0.7
