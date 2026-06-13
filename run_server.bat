@echo off
REM NeuroGemma Server Startup Script (No Docker)
REM This script activates the conda environment and starts the Streamlit app.

SET CONDA_ENV=neuro_env
SET MODEL_PATH=D:\modelos\MedTrinity25M_full\MedTrinity25M_full_55k\merged_model

echo [1/3] Checking environment...
call conda activate %CONDA_ENV%
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Conda environment '%CONDA_ENV%' not found. 
    echo Please run 'conda env create -f environment.yml' first.
    exit /b %ERRORLEVEL%
)

echo [2/3] Setting VLM model path...
SET VLM_MODEL_PATH=%MODEL_PATH%
echo Model path set to: %VLM_MODEL_PATH%

echo [3/3] Launching NeuroGemma...
streamlit run app.py --server.port=8501 --server.address=0.0.0.0

pause
