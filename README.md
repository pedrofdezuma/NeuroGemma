# NeuroGemma 🧠

**Advanced MRI Analysis & Clinical Decision Support System**

NeuroGemma is a modular monolith application designed to assist radiologists by providing automated MRI analysis using local AI models (CNNs and VLMs). It follows a strict privacy-first, local-inference-only architecture.

## Clinical Overview

NeuroGemma orchestrates a diagnostic pipeline:
1. **Axial-Flair Logic Gate:** Validates scan type and orientation.
2. **CNN Inference:** Identifies features and anomalies.
3. **MedGemma VLM:** Provides high-level clinical interpretation (4-bit quantized).
4. **Report Generation:** Produces professional radiology notes in PDF format.

## Technology Stack

- **Framework:** Streamlit
- **Runtime:** Python 3.12 (Conda)
- **Inference:** PyTorch, ONNX Runtime, Transformers, BitsAndBytes
- **Infrastructure:** Docker with NVIDIA Container Toolkit

## Getting Started

### Prerequisites

- NVIDIA GPU with 8GB+ VRAM recommended.
- [Conda](https://docs.conda.io/en/latest/miniconda.html) (Miniconda or Anaconda) installed.
- [Optional] Docker with NVIDIA Container Toolkit for deployment testing.

### Local Development (Conda) - Recommended

1. **Create the environment:**
   ```bash
   conda env create -f environment.yml
   ```

2. **Activate and run:**
   ```bash
   conda activate neuro_env
   streamlit run app.py
   ```

3. **Verify Installation:**
   ```bash
   python src/utils/verify_env.py
   ```

### Deployment Testing (Docker)

1. **Build the image:**
   ```bash
   docker build -t neurogemma .
   ```

2. **Run the container (with GPU support):**
   ```bash
   docker run --gpus all -p 8501:8501 neurogemma
   ```

## Project Structure

- `src/models/`: Inference Hub (Model wrappers)
- `src/logic/`: Orchestration Engine (Logic Gate)
- `src/reports/`: Reporting Engine (PDF Generation)
- `src/utils/`: Utilities & Styles
- `tests/`: Pytest suite

## License

Proprietary - Clinical Decision Support Tool
