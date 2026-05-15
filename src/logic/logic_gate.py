"""Orchestration logic for the NeuroGemma clinical pipeline."""
import streamlit as st
from datetime import datetime
from typing import Optional, Any
from PIL import Image
from src.logic.state import PipelineStage, reset_state, InferenceState
from src.utils.mock_data import get_mock_results
from src.models.model_medgemma_vlm import ModelMedGemmaVLM
from src.models.model_plane_cnn import ModelPlaneCNN
from src.models.model_seq_cnn import ModelSeqCNN
from src.models.model_depth_cnn import ModelDepthCNN

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

def run_pipeline(image: Image.Image) -> None:
    """
    Orchestrate the real inference pipeline for an uploaded image.
    
    Args:
        image: The PIL Image to process.
    """
    if "inference" not in st.session_state:
        from src.logic.state import init_state
        init_state()
    
    inference = st.session_state.inference
    inference.is_mock_mode = False
    inference.results = {} # Reset previous results
    inference.step_logs = [] # Reset previous logs
    
    # --- STAGE: ID (CNN Classification) ---
    inference.current_stage = PipelineStage.ID
    
    # 1. Plane CNN
    plane_model = ModelPlaneCNN()
    plane_res = plane_model.predict(image)
    inference.results["plane"] = plane_res["label"]
    
    inference.step_logs.append({
        "timestamp": datetime.now().isoformat(),
        "stage": "ID",
        "event": "PLANE_CLASSIFIED",
        "model_id": "plane_cnn",
        "outcome": plane_res["label"],
        "confidence": plane_res["confidence"],
        "metadata": {"raw_scores": plane_res.get("raw_scores")}
    })
    
    # 2. Sequence CNN
    seq_model = ModelSeqCNN()
    seq_res = seq_model.predict(image)
    inference.results["sequence"] = seq_res["label"]
    
    inference.step_logs.append({
        "timestamp": datetime.now().isoformat(),
        "stage": "ID",
        "event": "SEQUENCE_CLASSIFIED",
        "model_id": "seq_cnn",
        "outcome": seq_res["label"],
        "confidence": seq_res["confidence"],
        "metadata": {"raw_scores": seq_res.get("raw_scores")}
    })
    
    # 3. Depth CNN
    depth_model = ModelDepthCNN()
    depth_res = depth_model.predict(image)
    inference.results["depth"] = depth_res["label"]
    
    inference.step_logs.append({
        "timestamp": datetime.now().isoformat(),
        "stage": "ID",
        "event": "DEPTH_ESTIMATED",
        "model_id": "depth_cnn",
        "outcome": depth_res["label"],
        "confidence": depth_res["confidence"],
        "metadata": {"raw_scores": depth_res.get("raw_scores")}
    })
    
    # Calculate aggregate confidence (simple average)
    total_conf = plane_res["confidence"] + seq_res["confidence"] + depth_res["confidence"]
    inference.results["confidence"] = total_conf / 3
    
    # --- STAGE: GATE (Logic Gate Decision) ---
    inference.current_stage = PipelineStage.GATE
    evaluate_logic_gate(inference, image)
    
    # --- STAGE: COMPLETE ---
    inference.current_stage = PipelineStage.COMPLETE

def evaluate_logic_gate(inference_state: InferenceState, image: Image.Image) -> None:
    """
    Evaluate if the current scan warrants VLM narrative generation.
    
    Args:
        inference_state: The current state of the inference pipeline.
        image: The uploaded image object.
    """
    plane = str(inference_state.results.get("plane", "")).lower()
    sequence = str(inference_state.results.get("sequence", "")).lower()
    
    is_axial_flair = (plane == "axial" and sequence == "flair")
    outcome = "TRIGGERED" if is_axial_flair else "SKIPPED"
    
    # Log the decision
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "stage": "GATE",
        "event": "GATE_DECISION",
        "model_id": "logic_gate",
        "outcome": outcome,
        "confidence": 1.0,
        "metadata": {
            "plane": plane,
            "sequence": sequence
        }
    }
    inference_state.step_logs.append(log_entry)
    
    if is_axial_flair:
        # --- STAGE: SYNTHESIS ---
        inference_state.current_stage = PipelineStage.SYNTHESIS
        vlm = ModelMedGemmaVLM()
        prediction = vlm.predict(image)
        narrative = prediction.get("text", "No narrative generated.")
        inference_state.results["narrative"] = narrative
        
        # Log the VLM outcome
        inference_state.step_logs.append({
            "timestamp": datetime.now().isoformat(),
            "stage": "SYNTHESIS",
            "event": "NARRATIVE_GENERATED",
            "model_id": "medgemma_vlm",
            "outcome": "SUCCESS",
            "confidence": prediction.get("confidence", 1.0),
            "metadata": {"text_length": len(narrative)}
        })
    else:
        # Bypass VLM
        inference_state.results["narrative"] = "Analysis Skipped (Scan not Axial-FLAIR)"
        
        # Log the skip
        inference_state.step_logs.append({
            "timestamp": datetime.now().isoformat(),
            "stage": "GATE",
            "event": "SYNTHESIS_SKIPPED",
            "model_id": "medgemma_vlm",
            "outcome": "SKIPPED",
            "confidence": 1.0,
            "metadata": {"reason": "Logic gate requirements not met"}
        })
