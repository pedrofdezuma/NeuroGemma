# NeuroGemma 🧠

**Sistema Avanzado de Análisis de RM y Soporte a la Decisión Clínica**

NeuroGemma es una aplicación de monolito modular diseñada para asistir a radiólogos proporcionando análisis automatizado de resonancias magnéticas (RM) utilizando modelos de IA locales (CNNs y VLMs). Sigue una arquitectura estricta de privacidad primero, con inferencia únicamente local.

## Descripción Clínica

NeuroGemma orquesta un flujo de diagnóstico:
1. **Puerta Lógica Axial-Flair:** Valida el tipo de escaneo y la orientación.
2. **Inferencia CNN:** Identifica características y anomalías.
3. **MedGemma VLM:** Proporciona interpretación clínica de alto nivel (cuantizado a 4 bits).
4. **Generación de Informes:** Produce notas radiológicas profesionales en formato PDF.

## Stack Tecnológico

- **Framework:** Streamlit
- **Entorno de Ejecución:** Python 3.12 (Conda)
- **Inferencia:** PyTorch, ONNX Runtime, Transformers, BitsAndBytes

## Primeros Pasos

### Prerrequisitos

- Se recomienda una GPU NVIDIA con más de 8GB de VRAM.
- [Conda](https://docs.conda.io/en/latest/miniconda.html) (Miniconda o Anaconda) instalado.

### Desarrollo Local (Conda) - Recomendado

1. **Crear el entorno:**
   ```bash
   conda env create -f environment.yml
   ```

2. **Activar y ejecutar:**
   ```bash
   conda activate neuro_env
   streamlit run app.py
   ```

3. **Verificar la Instalación:**
   ```bash
   python src/utils/verify_env.py
   ```

## Estructura del Proyecto

- `src/models/`: Hub de Inferencia (Wrappers de modelos)
- `src/logic/`: Motor de Orquestación (Puerta Lógica)
- `src/reports/`: Motor de Informes (Generación de PDF)
- `src/utils/`: Utilidades y Estilos
- `tests/`: Suite de Pytest

## Licencia

Propietaria - Herramienta de Soporte a la Decisión Clínica
