import torch
from transformers import Gemma3ForConditionalGeneration, AutoProcessor, BitsAndBytesConfig
import os
import gc

def test_vlm_load_cpu():
    model_id = r"D:\modelos\MedTrinity25M_full\MedTrinity25M_full_55k\merged_model"
    print(f"Checking path: {model_id}")
    
    print("Attempting to load model on CPU only (to test data integrity)...")
    try:
        processor = AutoProcessor.from_pretrained(model_id)
        print("Processor loaded successfully.")
        
        # Load on CPU, no quantization for this test to avoid BNB issues
        model = Gemma3ForConditionalGeneration.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            device_map="cpu",
            low_cpu_mem_usage=True
        )
        print("Model loaded successfully on CPU.")
        print(f"Device: {model.device}")
    except Exception as e:
        print(f"FAILURE: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_vlm_load_cpu()
