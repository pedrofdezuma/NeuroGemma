#!/bin/bash
# NeuroGemma Server Startup Script (Linux/Ubuntu)

# 1. Configuración
CONDA_ENV="neuro_env"
# IMPORTANTE: Cambia esta ruta a la ubicación real del modelo en el servidor Ubuntu
MODEL_PATH="/home/pedrofernandez/modelos/MedTrinity25M_full/merged_model" 

echo "[1/3] Activando entorno Conda..."
# Cargar conda en el script de bash
source $(conda info --base)/etc/profile.d/conda.sh
conda activate $CONDA_ENV

if [ $? -ne 0 ]; then
    echo "[ERROR] No se pudo activar el entorno '$CONDA_ENV'."
    echo "Por favor, ejecuta: conda env create -f environment.yml"
    exit 1
fi

echo "[2/3] Configurando ruta del modelo..."
export VLM_MODEL_PATH=$MODEL_PATH
echo "Modelo configurado en: $VLM_MODEL_PATH"

echo "[3/3] Lanzando NeuroGemma..."
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
