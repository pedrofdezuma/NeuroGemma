from unittest.mock import MagicMock, patch
import pytest
from PIL import Image
from src.logic.logic_gate import run_pipeline
from src.logic.state import PipelineStage, InferenceState
import streamlit as st
from typing import Generator

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
def test_run_pipeline_as_generator(MockVLM, MockDepth, MockSeq, MockPlane):
    """Verify that run_pipeline is a generator and yields correct stages."""
    # Setup mocks
    mock_image = MagicMock(spec=Image.Image)
    
    # Force VLM trigger (axial + flair)
    MockPlane.return_value.predict.return_value = {"label": "axial", "confidence": 0.9}
    MockSeq.return_value.predict.return_value = {"label": "flair", "confidence": 0.8}
    MockDepth.return_value.predict.return_value = {"label": "slice_10", "confidence": 0.7}
    MockVLM.return_value.predict.return_value = {"text": "VLM output", "confidence": 0.95}
    
    # Initialize session state
    st.session_state.inference = InferenceState()
    
    # Execute - this should return a generator
    generator = run_pipeline(mock_image)
    
    # In RED phase, this will fail because run_pipeline returns None (currently)
    assert isinstance(generator, Generator), "run_pipeline should be a generator"
    
    stages_yielded = list(generator)
    
    # Verify expected stages
    expected_stages = [
        PipelineStage.ID,
        PipelineStage.GATE,
        PipelineStage.SYNTHESIS,
        PipelineStage.COMPLETE
    ]
    assert stages_yielded == expected_stages
    
    # Verify state updates at the end
    inference = st.session_state.inference
    assert inference.current_stage == PipelineStage.COMPLETE
    assert inference.results["narrative"] == "VLM output"
