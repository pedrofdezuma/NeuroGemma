"""Orchestration logic for the NeuroGemma clinical pipeline."""
import streamlit as st
from datetime import datetime
from typing import Optional, Any, Generator
from PIL import Image
from src.logic.state import PipelineStage, reset_state, InferenceState
from src.logic.exceptions import InferenceError, StageError
from src.utils.mock_data import get_mock_results
from src.models.model_medgemma_vlm import ModelMedGemmaVLM
from src.models.model_plane_cnn import ModelPlaneCNN
from src.models.model_seq_cnn import ModelSeqCNN
from src.models.model_depth_cnn import ModelDepthCNN

from src.utils.localization import get_text

def run_mock_inference(dataset_id: str) -> Generator[PipelineStage, None, None]:
    """
    Simulate the inference pipeline using a golden dataset.

    Args:
        dataset_id: The ID of the golden dataset to load.
    """
    # 1. Clear existing results
    # We must preserve the language before reset
    lang = st.session_state.inference.language
    reset_state()
    st.session_state.inference.language = lang
    
    # 2. Retrieve mock data
    try:
        mock_data = get_mock_results(dataset_id)
    except Exception as e:
        # If dataset_id is invalid, we might still want to proceed with an error
        mock_data = None
    
    if "inference" not in st.session_state:
        from src.logic.state import init_state
        init_state()

    inference = st.session_state.inference
    inference.is_mock_mode = True
    
    # Load specific mock image if available, else fallback to placeholder
    import os
    placeholder_color = (20, 20, 20)
    if mock_data and "image_path" in mock_data and os.path.exists(mock_data["image_path"]):
        try:
            inference.uploaded_image = Image.open(mock_data["image_path"])
        except Exception:
            inference.uploaded_image = Image.new('RGB', (512, 512), color=placeholder_color)
    else:
        inference.uploaded_image = Image.new('RGB', (512, 512), color=placeholder_color)
    
    # --- STAGE: ID ---
    inference.current_stage = PipelineStage.ID
    yield PipelineStage.ID
    
    if dataset_id == "error_scenario":
        inference.model_status["plane"] = "Processing"
        import time
        time.sleep(1) # Simulate some work
        inference.model_status["plane"] = "Error"
        inference.step_logs.append({
            "timestamp": datetime.now().isoformat(),
            "stage": "ID",
            "event": "ERROR",
            "model_id": "plane_cnn",
            "outcome": "FAILURE",
            "metadata": {"error": "Simulated model timeout"}
        })
        raise InferenceError("Simulated Plane Classification Failure")

    # 3. Populate results partially to simulate ID
    inference.model_status["plane"] = "Complete"
    inference.model_status["sequence"] = "Complete"
    inference.model_status["depth"] = "Complete"

    if mock_data:
        inference.results["plane"] = mock_data["plane"]
        inference.results["sequence"] = mock_data["sequence"]
        inference.results["depth"] = mock_data["depth"]
        inference.results["plane_conf"] = mock_data.get("plane_conf", 1.0)
        inference.results["sequence_conf"] = mock_data.get("sequence_conf", 1.0)
        inference.results["depth_conf"] = mock_data.get("depth_conf", 1.0)
        inference.results["confidence"] = mock_data["confidence"]
    
    # --- STAGE: GATE ---
    inference.current_stage = PipelineStage.GATE
    yield PipelineStage.GATE
    
    # Check if SYNTHESIS should happen in mock
    is_axial_flair = mock_data and (str(mock_data["plane"]).lower() == "axial" and 
                     str(mock_data["sequence"]).lower() == "flair")
    
    if is_axial_flair:
        # --- STAGE: SYNTHESIS ---
        inference.current_stage = PipelineStage.SYNTHESIS
        yield PipelineStage.SYNTHESIS
        inference.results["narrative"] = mock_data["narrative"]
        inference.model_status["narrative"] = "Complete"
    else:
        inference.results["narrative"] = get_text("vlm_skipped_reason", lang)
        inference.model_status["narrative"] = "Skipped"
    
    # 4. Populate step logs
    if mock_data:
        inference.step_logs = []
        for log_entry in mock_data["logs"]:
            full_log = log_entry.copy()
            full_log["timestamp"] = datetime.now().isoformat()
            inference.step_logs.append(full_log)
    
    # 5. Set final stage
    inference.current_stage = PipelineStage.COMPLETE
    yield PipelineStage.COMPLETE

def run_pipeline(image: Image.Image) -> Generator[PipelineStage, None, None]:
    """
    Orchestrate the real inference pipeline for an uploaded image.
    
    Args:
        image: The PIL Image to process.
    """
    if "inference" not in st.session_state:
        from src.logic.state import init_state
        init_state()
    
    inference = st.session_state.inference
    lang = inference.language
    inference.is_mock_mode = False
    inference.results = {} 
    inference.step_logs = [] 
    
    # --- STAGE: ID (CNN Classification) ---
    inference.current_stage = PipelineStage.ID
    yield PipelineStage.ID
    
    # 1. Plane CNN
    inference.model_status["plane"] = "Processing"
    try:
        plane_model = ModelPlaneCNN()
        plane_res = plane_model.predict(image)
        inference.results["plane"] = plane_res["label"]
        inference.results["plane_conf"] = plane_res["confidence"]
        inference.model_status["plane"] = "Complete"
        
        inference.step_logs.append({
            "timestamp": datetime.now().isoformat(),
            "stage": "ID",
            "event": "PLANE_CLASSIFIED",
            "model_id": "plane_cnn",
            "outcome": plane_res["label"],
            "confidence": plane_res["confidence"],
            "metadata": {"raw_scores": plane_res.get("raw_scores")}
        })
    except Exception as e:
        inference.model_status["plane"] = "Error"
        inference.step_logs.append({
            "timestamp": datetime.now().isoformat(),
            "stage": "ID",
            "event": "ERROR",
            "model_id": "plane_cnn",
            "outcome": "FAILURE",
            "metadata": {"error": str(e)}
        })
        raise InferenceError(f"Plane Classification Failed: {str(e)}") from e
    
    # 2. Sequence CNN
    inference.model_status["sequence"] = "Processing"
    try:
        seq_model = ModelSeqCNN()
        seq_res = seq_model.predict(image)
        inference.results["sequence"] = seq_res["label"]
        inference.results["sequence_conf"] = seq_res["confidence"]
        inference.model_status["sequence"] = "Complete"
        
        inference.step_logs.append({
            "timestamp": datetime.now().isoformat(),
            "stage": "ID",
            "event": "SEQUENCE_CLASSIFIED",
            "model_id": "seq_cnn",
            "outcome": seq_res["label"],
            "confidence": seq_res["confidence"],
            "metadata": {"raw_scores": seq_res.get("raw_scores")}
        })
    except Exception as e:
        inference.model_status["sequence"] = "Error"
        inference.step_logs.append({
            "timestamp": datetime.now().isoformat(),
            "stage": "ID",
            "event": "ERROR",
            "model_id": "seq_cnn",
            "outcome": "FAILURE",
            "metadata": {"error": str(e)}
        })
        raise InferenceError(f"Sequence Classification Failed: {str(e)}") from e
    
    # 3. Depth CNN
    inference.model_status["depth"] = "Processing"
    try:
        depth_model = ModelDepthCNN()
        filename = inference.image_metadata.get("filename", "")
        depth_res = depth_model.predict(image, filename=filename)
        inference.results["depth"] = depth_res["label"]
        inference.results["depth_conf"] = depth_res["confidence"]
        inference.model_status["depth"] = "Complete"
        
        inference.step_logs.append({
            "timestamp": datetime.now().isoformat(),
            "stage": "ID",
            "event": "DEPTH_ESTIMATED",
            "model_id": "depth_cnn",
            "outcome": depth_res["label"],
            "confidence": depth_res["confidence"],
            "metadata": {"raw_scores": depth_res.get("raw_scores")}
        })
    except Exception as e:
        inference.model_status["depth"] = "Error"
        inference.step_logs.append({
            "timestamp": datetime.now().isoformat(),
            "stage": "ID",
            "event": "ERROR",
            "model_id": "depth_cnn",
            "outcome": "FAILURE",
            "metadata": {"error": str(e)}
        })
        raise InferenceError(f"Depth Estimation Failed: {str(e)}") from e
    
    # Calculate aggregate confidence (Average of classification models only)
    plane_conf = inference.results.get("plane_conf", 0.0)
    seq_conf = inference.results.get("sequence_conf", 0.0)
    inference.results["confidence"] = (plane_conf + seq_conf) / 2
    
    # --- STAGE: GATE (Logic Gate Decision) ---
    inference.current_stage = PipelineStage.GATE
    yield PipelineStage.GATE
    
    yield from evaluate_logic_gate(inference, image)
    
    # --- STAGE: COMPLETE ---
    inference.current_stage = PipelineStage.COMPLETE
    yield PipelineStage.COMPLETE

def evaluate_logic_gate(inference_state: InferenceState, image: Image.Image) -> Generator[PipelineStage, None, None]:
    """
    Evaluate if the current scan warrants VLM narrative generation.
    
    Args:
        inference_state: The current state of the inference pipeline.
        image: The uploaded image object.
    """
    lang = inference_state.language
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
        yield PipelineStage.SYNTHESIS
        
        inference_state.model_status["narrative"] = "Processing"
        try:
            vlm = ModelMedGemmaVLM()
            prediction = vlm.predict(image)
            narrative = prediction.get("text", "No narrative generated.")
            inference_state.results["narrative"] = narrative
            
            # If the model is disabled, we mark it as 'Skipped' or 'Disabled' instead of 'Complete'
            if "disabled" in narrative.lower():
                inference_state.model_status["narrative"] = "Skipped"
                outcome = "DISABLED"
            else:
                inference_state.model_status["narrative"] = "Complete"
                outcome = "SUCCESS"
            
            # Log the VLM outcome
            inference_state.step_logs.append({
                "timestamp": datetime.now().isoformat(),
                "stage": "SYNTHESIS",
                "event": "NARRATIVE_GENERATED",
                "model_id": "medgemma_vlm",
                "outcome": outcome,
                "confidence": prediction.get("confidence", 1.0),
                "metadata": {"text_length": len(narrative)}
            })
        except Exception as e:
            inference_state.model_status["narrative"] = "Error"
            inference_state.step_logs.append({
                "timestamp": datetime.now().isoformat(),
                "stage": "SYNTHESIS",
                "event": "ERROR",
                "model_id": "medgemma_vlm",
                "outcome": "FAILURE",
                "metadata": {"error": str(e)}
            })
            raise InferenceError(f"VLM Synthesis Failed: {str(e)}") from e
    else:
        # Bypass VLM
        inference_state.results["narrative"] = get_text("vlm_skipped_reason", lang)
        inference_state.model_status["narrative"] = "Skipped"
        
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
