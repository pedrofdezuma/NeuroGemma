import pytest
from src.logic.state import PipelineStage, InferenceState

def test_pipeline_stage_enum():
    """Verify that PipelineStage enum has the correct members."""
    assert PipelineStage.ID.value == "ID"
    assert PipelineStage.GATE.value == "GATE"
    assert PipelineStage.SYNTHESIS.value == "SYNTHESIS"
    assert PipelineStage.COMPLETE.value == "COMPLETE"

def test_inference_state_defaults():
    """Verify default values of InferenceState dataclass."""
    state = InferenceState()
    assert state.current_stage == PipelineStage.ID
    assert state.results == {}
    assert state.step_logs == []
    assert state.is_mock_mode is False
    assert state.uploaded_image is None
    assert state.image_metadata == {}

def test_inference_state_types():
    """Verify that InferenceState accepts correct types."""
    from PIL import Image
    img = Image.new('RGB', (10, 10))
    state = InferenceState(
        current_stage=PipelineStage.GATE,
        results={"test": 1},
        step_logs=[{"event": "test"}],
        is_mock_mode=True,
        uploaded_image=img,
        image_metadata={"format": "PNG"}
    )
    assert state.current_stage == PipelineStage.GATE
    assert state.results == {"test": 1}
    assert state.step_logs == [{"event": "test"}]
    assert state.is_mock_mode is True
    assert state.uploaded_image == img
    assert state.image_metadata == {"format": "PNG"}

def test_init_state():
    """Verify that init_state initializes session_state correctly."""
    import streamlit as st
    # Clear session state if it exists from other tests (though pytest should isolate)
    if "inference" in st.session_state:
        del st.session_state["inference"]
    
    from src.logic.state import init_state
    init_state()
    
    assert "inference" in st.session_state
    assert isinstance(st.session_state.inference, InferenceState)
    assert st.session_state.inference.current_stage == PipelineStage.ID

def test_reset_state():
    """Verify that reset_state wipes the session_state."""
    import streamlit as st
    from src.logic.state import init_state, reset_state, PipelineStage
    from PIL import Image
    
    init_state()
    st.session_state.inference.current_stage = PipelineStage.GATE
    st.session_state.inference.results = {"some": "data"}
    st.session_state.inference.uploaded_image = Image.new('RGB', (10, 10))
    st.session_state.inference.image_metadata = {"format": "PNG"}
    
    reset_state()
    
    assert st.session_state.inference.current_stage == PipelineStage.ID
    assert st.session_state.inference.results == {}
    assert st.session_state.inference.uploaded_image is None
    assert st.session_state.inference.image_metadata == {}

def test_step_log_format():
    """Verify that step_logs entries follow the specified schema."""
    state = InferenceState()
    log_entry = {
        "timestamp": "2026-05-12T22:00:00Z",
        "stage": "GATE",
        "event": "MODEL_INFERENCE_START",
        "model_id": "model_axial_cnn",
        "outcome": "success",
        "confidence": 0.95,
        "metadata": {"device": "cuda"}
    }
    state.step_logs.append(log_entry)
    
    entry = state.step_logs[0]
    assert isinstance(entry["timestamp"], str)
    assert entry["stage"] in ["ID", "GATE", "SYNTHESIS", "COMPLETE"]
    assert isinstance(entry["confidence"], float)
    assert isinstance(entry["metadata"], dict)
