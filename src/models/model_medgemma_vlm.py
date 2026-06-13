import torch
import streamlit as st
import warnings
import logging
import gc
from PIL import Image
from transformers import (
    AutoModelForImageTextToText,
    AutoProcessor, 
    BitsAndBytesConfig
)
from typing import Any

# Suppress verbose transformers warnings about path access
warnings.filterwarnings("ignore", category=UserWarning, module="transformers.models.auto.image_processing_auto")
logging.getLogger("transformers").setLevel(logging.ERROR)

PROMPT_EN = """You are provided with this brain MRI image from a medical dataset.
Your task is to answer the following questions based on the image and green bounding box, and condense your answers into caption-styled text.
###question1
Give me a detailed description of the image, including type of the image, organs in the image, approximate location of these organs and relevant locations of these organs and any medical devices (if present) visible in the image as detailedly as possible.
Note when answering question1:
1. It is irrelevant for this question whether the image depicts a lesion or not. The answer should be the same.
2. Your answer should not contain anything about the green bounding box like the contour itself and its outline.
3. Do not explain or emphasize your analysis.
###question2
Identify and describe any lesions visible in the image, if present. These lesions may be indicated by green bounding boxes; in such cases, prioritize describing the specific regions within these boxes. For each lesion, specify its exact anatomical location and its position relative to reference structures. Describe what is unusual in those regions, providing details on signal intensity, texture, size, and other morphological features.
Note when answering question2:
1. If one or more green bounding boxes are present, they indicate regions of interest; prioritize identifying and describing the pathological findings within every provided bounding box.
2. If no lesion is visible in the image or within the bounding boxes, explicitly state that the image shows no visible lesion.
3. Do not mention the box's physical attributes (e.g., "green line", "contour", or "square outline").
4. Do not use phrase "green bounding box" in your response, use "region of interest" as a substitution.
5. If multiple lesions or bounding boxes exist, ensure each is described individually to maintain a comprehensive clinical description.
6. Do not say anything that is not needed in your analysis, like introduction of the disease and medical equipments.
7. Do not explain or emphasize your analysis.
###question3
Specify the relationship between the identified lesion(s) and other anatomical regions, explaining the underlying cause of this interaction and its clinical probability.
Note when answering question3:
1. Answer this question only if a lesion is present in the image. If no lesion is visible, provide no response for this section.
2. The response must be highly condensed, limited to a maximum of 2 lines.
3. Do not emphasize your analysis.
###Consolidated Clinical Narrative
Synthesize the findings from the three previous questions into a single, fluid paragraph. Avoid a "Question-Answer" format or bullet points. The final output must be a cohesive and slightly condensed descriptive summary that preserves all essential medical details and observations.
"""

PROMPT_ES = """Se te proporciona esta imagen de resonancia magnética cerebral de un conjunto de datos médicos.
Tu tarea es responder a las siguientes preguntas basadas en la imagen y el cuadro delimitador verde, y condensar tus respuestas en un texto de estilo pie de foto.
###pregunta1
Dame una descripción detallada de la imagen, incluyendo el tipo de imagen, los órganos en la imagen, la ubicación aproximada de estos órganos y las ubicaciones relevantes de estos órganos y cualquier dispositivo médico (si está presente) visible en la imagen con el mayor detalle posible.
Nota al responder a la pregunta 1:
1. Es irrelevante para esta pregunta si la imagen muestra una lesión o no. La respuesta debe ser la misma.
2. Tu respuesta no debe contener nada sobre el cuadro delimitador verde, como el contorno en sí y su perfil.
3. No expliques ni enfatices tu análisis.
###pregunta2
Identifica y describe cualquier lesión visible en la imagen, si está presente. Estas lesiones pueden estar indicadas por cuadros delimitadores verdes; en tales casos, prioriza la descripción de las regiones específicas dentro de estos cuadros. Para cada lesión, especifica su ubicación anatómica exacta y su posición con respecto a las estructuras de referencia. Describe qué es inusual en esas regiones, proporcionando detalles sobre la intensidad de la señal, la textura, el tamaño y otras características morfológicas.
Nota al responder a la pregunta 2:
1. Si uno o más cuadros delimitadores verdes están presentes, indican regiones de interés; prioriza la identificación y descripción de los hallazgos patológicos dentro de cada cuadro delimitador proporcionado.
2. Si no es visible ninguna lesión en la imagen o dentro de los cuadros delimitadores, indica explícitamente que la imagen no muestra ninguna lesión visible.
3. No menciones los atributos físicos del cuadro (por ejemplo, "línea verde", "contorno" o "perfil cuadrado").
4. No utilices la frase "cuadro delimitador verde" en tu respuesta, utiliza "región de interés" como sustitución.
5. Si existen múltiples lesiones o cuadros delimitadores, asegúrate de que cada uno se describa individualmente para mantener una descripción clínica exhaustiva.
6. No digas nada que no sea necesario en tu análisis, como la introducción de la enfermedad y los equipos médicos.
7. No expliques ni enfatices tu análisis.
###pregunta3
Especifica la relación entre la(s) lesión(es) identificada(s) y otras regiones anatómicas, explicando la causa subyacente de esta interacción y su probabilidad clínica.
Nota al responder a la pregunta 3:
1. Responde a esta pregunta solo si hay una lesión presente en la imagen. Si no hay ninguna lesión visible, no proporciones ninguna respuesta para esta sección.
2. La respuesta debe estar altamente condensada, limitada a un máximo de 2 líneas.
3. No enfatices tu análisis.
###Narrativa Clínica Consolidada
Sintetiza los hallazgos de las tres preguntas anteriores en un único párrafo fluido. Evita el formato de "Pregunta-Respuesta" o los puntos. El resultado final debe ser un resumen descriptivo cohesivo y ligeramente condensado que preserve todos los detalles médicos y observaciones esenciales. Escribe la respuesta final obligatoriamente en Español.
"""

@st.cache_resource
def load_vlm_model(model_id: str):
    """Loads the VLM model and processor with 4-bit quantization for efficiency."""
    try:
        # Check if we have a GPU
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # 4-bit Quantization Config (Based on user's known working config)
        quantization_config = None
        if device == "cuda":
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
                bnb_4bit_compute_dtype=torch.bfloat16, # bfloat16 is better for MedGemma/Picasso
                llm_int8_enable_fp32_cpu_offload=True
            )

        processor = AutoProcessor.from_pretrained(model_id)
        
        # Use bfloat16 if available (Ampere GPUs like A100/H100)
        torch_dtype = torch.bfloat16 if device == "cuda" else torch.float32

        model = AutoModelForImageTextToText.from_pretrained(
            model_id,
            quantization_config=quantization_config,
            device_map="auto",
            torch_dtype=torch_dtype,
            low_cpu_mem_usage=True
        )
        return model, processor, None
    except Exception as e:
        error_msg = f"Failed to load VLM: {str(e)}"
        logging.error(error_msg)
        return None, None, error_msg

class ModelMedGemmaVLM:
    """Wrapper for the MedGemma VLM model."""

    def __init__(self, model_id: str = None):
        """Initialize the VLM wrapper."""
        import os
        # Default to the Ubuntu server path
        self.model_id = model_id or os.getenv("VLM_MODEL_PATH", "/home/pedrofernandez/modelos/merged_model")
        self.model, self.processor, self.load_error = load_vlm_model(self.model_id)

    def predict(self, image: Image.Image, lang: str = "English") -> dict[str, Any]:
        """Perform inference using the VLM."""
        if self.model is None or self.processor is None:
            return {
                "label": "Error",
                "text": f"VLM could not be loaded. {self.load_error or 'Check model path.'}",
                "confidence": 0.0
            }

        try:
            # Select prompt based on language
            base_prompt = PROMPT_ES if lang == "Español" else PROMPT_EN
            
            # Gemma 3 and modern MedTrinity models use a chat template to handle multimodal inputs correctly.
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image"},
                        {"type": "text", "text": base_prompt},
                    ],
                }
            ]
            
            # 1. Prepare inputs and measure input length
            prompt_text = self.processor.apply_chat_template(messages, add_generation_prompt=True, tokenize=False)
            inputs = self.processor(text=prompt_text, images=image, return_tensors="pt").to(self.model.device)
            input_len = inputs["input_ids"].shape[-1]
            
            # 2. Generate with user's specific parameters
            with torch.no_grad():
                output_ids = self.model.generate(
                    **inputs,
                    max_new_tokens=512,
                    do_sample=True,
                    temperature=0.1,
                    top_p=0.9,
                    use_cache=True
                )
            
            # 3. Slice and Decode (Critical for avoiding empty/repeated output)
            new_content_ids = output_ids[0][input_len:]
            generated_text = self.processor.decode(new_content_ids, skip_special_tokens=True).strip()

            # Debugging logs
            print(f"--- VLM INFERENCE DEBUG ({lang}) ---", flush=True)
            print(f"Generated text length: {len(generated_text)}", flush=True)
            
            if not generated_text:
                generated_text = "The model generated an empty response. Check if the image contains valid features."

            return {
                "label": "Narrative",
                "text": generated_text,
                "confidence": 1.0 
            }
        except Exception as e:
            logging.error(f"Inference error: {str(e)}")
            return {
                "label": "Error",
                "text": f"Error during VLM inference: {str(e)}",
                "confidence": 0.0
            }
