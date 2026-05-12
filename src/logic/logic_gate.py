"""Orchestration logic for the NeuroGemma clinical pipeline."""
import streamlit as st
from datetime import datetime
from typing import Optional
from src.logic.state import PipelineStage, reset_state
from src.utils.mock_data import get_mock_results

def run_mock_inference(dataset_id: str) -> None:
    """
    Simulate the inference pipeline using a golden dataset.

    Args:
        dataset_id: The ID of the golden dataset to load.
    """
    # 1. Clear existing results (reset state to clean slate)
    reset_state()
    
    # 2. Retrieve mock data
    mock_data = get_mock_results(dataset_id)
    
    # Ensure state is initialized (though reset_state does it)
    if "inference" not in st.session_state:
        from src.logic.state import init_state
        init_state()

    inference = st.session_state.inference
    inference.is_mock_mode = True
    
    # 3. Populate results
    inference.results = {
        "plane": mock_data["plane"],
        "sequence": mock_data["sequence"],
        "depth": mock_data["depth"],
        "narrative": mock_data["narrative"],
        "confidence": mock_data["confidence"]
    }
    
    # 4. Populate step logs with timestamps
    inference.step_logs = []
    for log_entry in mock_data["logs"]:
        # Add timestamp to each log entry
        full_log = log_entry.copy()
        full_log["timestamp"] = datetime.now().isoformat()
        inference.step_logs.append(full_log)
    
    # 5. Set final stage
    inference.current_stage = PipelineStage.COMPLETE
