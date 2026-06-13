import torch
from transformers import Gemma3ForConditionalGeneration, AutoProcessor, BitsAndBytesConfig
import os
import gc

def test_vlm_load_gpu_offload():
    model_id = r"D:\modelos\MedTrinity25M_full\MedTrinity25M_full_55k\merged_model"
    print(f"Checking path: {model_id}")
    
    # 4GB VRAM Optimization
    print("Attempting to load model with 4-bit quantization and CPU offload for 4GB VRAM...")
    try:
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.float16,
            llm_int8_enable_fp32_cpu_offload=True
        )

        processor = AutoProcessor.from_pretrained(model_id)
        print("Processor loaded successfully.")
        
        model = Gemma3ForConditionalGeneration.from_pretrained(
            model_id,
            quantization_config=quantization_config,
            device_map="auto", # Required for splitting across 4GB VRAM
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True
        )
        print("Model loaded successfully!")
        print(f"Model dispatch: {model.hf_device_map}")
        
    except Exception as e:
        print(f"FAILURE: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_vlm_load_gpu_offload()
