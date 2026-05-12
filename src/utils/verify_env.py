import torch
import onnxruntime as ort
import streamlit as st
import sys

def verify_environment() -> None:
    """
    Verifies the local execution environment for GPU and critical library availability.
    Prints status to console.
    """
    print("--- NeuroGemma Environment Verification ---")
    print(f"Python version: {sys.version}")
    
    # Check PyTorch & CUDA
    cuda_available = torch.cuda.is_available()
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA Available: {cuda_available}")
    if cuda_available:
        print(f"GPU Device: {torch.cuda.get_device_name(0)}")
    
    # Check ONNX Runtime
    providers = ort.get_available_providers()
    print(f"ONNX Runtime version: {ort.__version__}")
    print(f"ONNX Providers: {providers}")
    if 'CUDAExecutionProvider' in providers:
        print("✅ ONNX GPU acceleration available.")
    else:
        print("⚠️ ONNX GPU acceleration NOT found (using CPU).")
        
    # Check Streamlit
    print(f"Streamlit version: {st.__version__}")
    
    print("------------------------------------------")

if __name__ == "__main__":
    verify_environment()
