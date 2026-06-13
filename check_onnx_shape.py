import onnxruntime as ort
import sys

def check_model(path):
    try:
        session = ort.InferenceSession(path)
        print(f"Model: {path}")
        for input in session.get_inputs():
            print(f"Input Name: {input.name}")
            print(f"Input Shape: {input.shape}")
            print(f"Input Type: {input.type}")
    except Exception as e:
        print(f"Error loading {path}: {e}")

if __name__ == "__main__":
    check_model("models/depth_cnn.onnx")
