import onnxruntime as ort
import numpy as np
import streamlit as st
import os
from PIL import Image
from typing import Any

@st.cache_resource
def load_onnx_session(model_path: str) -> ort.InferenceSession:
    """Load an ONNX session and cache it."""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at: {os.path.abspath(model_path)}")
    
    # Use CPU by default to ensure compatibility
    providers = ['CPUExecutionProvider']
    return ort.InferenceSession(model_path, providers=providers)

class ModelPlaneCNN:
    """Wrapper for the Anatomical Plane CNN model (Axial/Sagittal/Coronal)."""

    def __init__(self, model_path: str = "models/plane_cnn.onnx"):
        self.model_path = model_path
        self.labels = ['axial', 'coronal', 'sagittal', 'non_brain_mri']
        try:
            self.session = load_onnx_session(self.model_path)
            self.error = None
        except Exception as e:
            self.session = None
            self.error = str(e)

    def _preprocess(self, image: Image.Image) -> np.ndarray:
        """
        Standard ImageNet-style preprocessing (224x224) 
        aligned with the training script normalization.
        """
        # 1. Resize and convert to RGB
        img = image.convert("RGB").resize((224, 224), resample=Image.Resampling.BILINEAR)
        img_data = np.array(img).astype(np.float32) / 255.0
        
        # 2. ImageNet Normalization (from training script)
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        img_data = (img_data - mean) / std
        
        # 3. Transpose to (C, H, W) and add batch dimension
        img_data = img_data.transpose(2, 0, 1)
        img_data = np.expand_dims(img_data, axis=0).astype(np.float32)
        return img_data

    def _softmax(self, x: np.ndarray) -> np.ndarray:
        """Compute softmax values for each sets of scores in x."""
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=1, keepdims=True)

    def predict(self, image: Image.Image) -> dict[str, Any]:
        """Classify the anatomical plane of the given image."""
        if self.session is None:
            return {
                "label": f"Load Error: {self.error}" if self.error else "Unknown",
                "confidence": 0.0,
                "raw_scores": []
            }

        try:
            input_name = self.session.get_inputs()[0].name
            
            # RE-ENABLING PREPROCESSING
            processed_img = self._preprocess(image)
            
            if processed_img.shape != (1, 3, 224, 224):
                raise ValueError(f"Preprocessing yielded invalid shape: {processed_img.shape}")
            
            raw_results = self.session.run(None, {input_name: processed_img})
            logits = raw_results[0]
            probs = self._softmax(logits)[0]
            
            idx = np.argmax(probs)
            label = self.labels[idx] if idx < len(self.labels) else f"Unknown (idx:{idx})"
            confidence = float(probs[idx])
            
            return {
                "label": label,
                "confidence": confidence,
                "raw_scores": probs.tolist()
            }
        except Exception as e:
            return {
                "label": f"Inference Error: {str(e)}",
                "confidence": 0.0,
                "raw_scores": []
            }
