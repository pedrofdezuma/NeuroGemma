import onnxruntime as ort
import numpy as np
import streamlit as st
import os
from PIL import Image, ImageOps
from typing import Any
from src.models.model_plane_cnn import load_onnx_session

class ModelDepthCNN:
    """Wrapper for the MRI Depth CNN model (Normalized Regression)."""

    def __init__(self, model_path: str = "models/depth_cnn.onnx"):
        self.model_path = model_path
        try:
            self.session = load_onnx_session(self.model_path)
            self.error = None
        except Exception as e:
            self.session = None
            self.error = str(e)

    def _preprocess(self, image: Image.Image, filename: str = "") -> np.ndarray:
        """
        Preprocessing with centered crop to 182x218, then padded to 224x224
        as required by the model, including conditional rotation.
        """
        img = image.convert("RGB")

        # Rotate 90 degrees clockwise if it's a BraTS sample
        if filename.lower().startswith("brats-"):
            img = img.transpose(Image.ROTATE_270)

        # 1. Centered crop and resize to target effective dimensions (182x218)
        img = ImageOps.fit(img, (182, 218), method=Image.Resampling.BILINEAR)
        
        # 2. Pad to 224x224 (required by ONNX model input shape)
        final_img = Image.new("RGB", (224, 224), (0, 0, 0))
        left = (224 - 182) // 2
        top = (224 - 218) // 2
        final_img.paste(img, (left, top))
        img = final_img
        
        # 3. Autocontrast: Normalize intensities to full [0, 255] range
        # This helps the model 'see' features in scans with different brightness/contrast levels.
        img = ImageOps.autocontrast(img)
        
        img_data = np.array(img).astype(np.float32) / 255.0
        
        # 4. ImageNet Normalization (from training script)
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        img_data = (img_data - mean) / std
        
        # 5. Transpose to (C, H, W) and add batch dimension
        img_data = img_data.transpose(2, 0, 1)
        img_data = np.expand_dims(img_data, axis=0).astype(np.float32)
        return img_data

    def predict(self, image: Image.Image, filename: str = "") -> dict[str, Any]:
        """Perform normalized depth regression on the given image."""
        if self.session is None:
            return {
                "label": 0.0,
                "confidence": 0.0,
                "error": self.error if self.error else "Unknown Load Error",
                "raw_scores": [0.0]
            }

        try:
            input_name = self.session.get_inputs()[0].name
            
            # RE-ENABLING PREPROCESSING
            processed_img = self._preprocess(image, filename=filename)
            
            if processed_img.shape != (1, 3, 224, 224):
                raise ValueError(f"Preprocessing yielded invalid shape: {processed_img.shape}")
            
            raw_results = self.session.run(None, {input_name: processed_img})
            depth_val = float(raw_results[0].item())
            
            # No clipping applied, returning raw model output
            
            return {
                "label": depth_val,
                "confidence": 1.0,
                "raw_scores": [depth_val]
            }
        except Exception as e:
            return {
                "label": 0.0,
                "confidence": 0.0,
                "error": str(e),
                "raw_scores": []
            }
