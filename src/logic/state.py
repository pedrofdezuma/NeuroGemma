from dataclasses import dataclass, field
from enum import Enum
import streamlit as st
from datetime import datetime

class PipelineStage(Enum):
    """Enumeration of clinical pipeline stages for UI breadcrumbs."""
    ID = "ID"
    GATE = "GATE"
    SYNTHESIS = "SYNTHESIS"
    COMPLETE = "COMPLETE"

@dataclass
class InferenceState:
    """Centralized state object for tracking inference progress and results."""
    current_stage: PipelineStage = PipelineStage.ID
    results: dict[str, any] = field(default_factory=dict)
    step_logs: list[dict[str, any]] = field(default_factory=list)
    is_mock_mode: bool = False

def init_state() -> None:
    """Initialize the InferenceState in Streamlit session state if not already present."""
    if "inference" not in st.session_state:
        st.session_state.inference = InferenceState()

def reset_state() -> None:
    """Reset the inference state to default values for privacy and new sessions."""
    st.session_state.inference = InferenceState()
