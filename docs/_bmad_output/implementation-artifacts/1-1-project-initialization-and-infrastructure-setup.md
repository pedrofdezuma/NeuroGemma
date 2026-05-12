# Story 1.1: Project Initialization and Infrastructure Setup

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Developer,
I want to initialize the project with a modular monolith structure and Docker configuration,
so that I have a consistent, GPU-ready environment for development and deployment.

## Acceptance Criteria

1. **Directory Structure:** The standard "Modular Monolith" directory structure is created (src/models, src/logic, src/reports, src/utils).
2. **Infrastructure:** The `Dockerfile` and `environment.yml` (Conda) are configured with NVIDIA-container-toolkit support and all necessary dependencies.
3. **Entry Point:** `app.py` is established as the Streamlit entry point with basic layout configuration.

## Tasks / Subtasks

- [x] **Initialize directory structure** (AC: #1)
  - [x] Create root directories: `src/models`, `src/logic`, `src/reports`, `src/utils`, `tests`
  - [x] Add `__init__.py` files to ensure they are treated as Python packages
- [x] **Configure Conda environment** (AC: #2)
  - [x] Create `environment.yml` with:
    - name: neuro_env
    - channels: [conda-forge, defaults]
    - dependencies:
      - python=3.12
      - pip
      - pip:
        - --index-url https://download.pytorch.org/whl/cu121
        - torch
        - torchvision
        - torchaudio
        - onnxruntime-gpu
        - transformers
        - bitsandbytes
        - accelerate
        - fpdf2
        - streamlit
        - pytest
        - black
        - ruff
- [x] **Configure Docker environment** (AC: #2)
  - [x] Create `Dockerfile` using `nvidia/cuda:12.1.0-base-ubuntu22.04`
  - [x] Install system dependencies (libgl1, libglib2.0-0, wget, git)
  - [x] Install Miniconda and setup `neuro_env`
  - [x] Configure `ENTRYPOINT` to run Streamlit via the conda environment
- [x] **Initialize Streamlit entry point** (AC: #3)
  - [x] Create `app.py` with basic tab layout: "Diagnostic View" and "Technical Logs"
  - [x] Implement global page config (Medical Blue theme)
  - [x] Add a placeholder sidebar with "Mock Mode" and "Clear Session" (logic in 1.4)
- [x] **Environment Verification & Documentation** (AC: #2)
  - [x] Create `src/utils/verify_env.py` to check GPU, CUDA, and library availability
  - [x] Create `README.md` with Docker build/run instructions and clinical overview
- [x] **Configure Streamlit theme** (AC: #3)
  - [x] Create `.streamlit/config.toml` with:
    - primaryColor = "#007BFF" (Medical Blue)
    - backgroundColor = "#F8F9FA" (Calm Slate)
    - secondaryBackgroundColor = "#E9ECEF"
    - textColor = "#2C3E50" (Soft Navy)
    - font = "sans serif"

## Dev Notes

### Architecture & Standards
- **Modular Monolith:** Strict separation of concerns. UI logic stays in `app.py`, business logic in `src/logic`, and model handling in `src/models`. [Source: docs/_bmad_output/planning-artifacts/architecture.md#Starter Template Evaluation]
- **GPU Readiness:** Environment must support local inference using ONNX (CNNs) and Transformers (4-bit MedGemma VLM).
- **Strict Typing:** All new Python code must use type hints. [Source: docs/_bmad_output/project-context.md#Language-Specific Rules]

### Implementation Guardrails
- **NO External APIs:** All inference must be local.
- **Privacy First:** Session reset policy must be prepared (state management will follow in 1.2).
- **Modular Boundaries:** `src/logic/` must not import `streamlit`.

### Project Structure Notes
- **Unified Structure:**
  - `src/models/`: Inference Hub (CNNs & VLM)
  - `src/logic/`: Orchestration Engine (Logic Gate)
  - `src/reports/`: Reporting Engine (fpdf2)
  - `src/utils/`: Utilities (File validation, Mock Mode, Styles)

## References

- **PRD:** [docs/_bmad_output/planning-artifacts/prd.md#Executive Summary]
- **Architecture:** [docs/_bmad_output/planning-artifacts/architecture.md#Starter Template Evaluation]
- **UX Design:** [docs/_bmad_output/planning-artifacts/ux-design-specification.md#5. Design System Foundation]
- **Project Context:** [docs/_bmad_output/project-context.md#Technology Stack & Versions]

## Dev Agent Record

### Agent Model Used

Gemini 2.0 Flash

### Debug Log References

### Completion Notes List
- Initialized modular monolith directory structure with `__init__.py` files.
- Configured `environment.yml` with all required AI and web dependencies.
- Created a production-ready `Dockerfile` based on NVIDIA CUDA 12.1.
- Implemented `app.py` with the required tab layout and global page configuration.
- Added `src/utils/verify_env.py` for environment health checks.
- Configured Streamlit theme in `.streamlit/config.toml`.
- Provided a comprehensive `README.md` with setup instructions.

### File List
- app.py
- Dockerfile
- environment.yml
- .streamlit/config.toml
- src/models/__init__.py
- src/logic/__init__.py
- src/reports/__init__.py
- src/utils/__init__.py
- src/utils/verify_env.py
- tests/__init__.py
- README.md

### Review Findings

- [ ] [Review][Patch] Missing .dockerignore [Dockerfile]
- [ ] [Review][Patch] Missing DICOM support libraries (pydicom) [environment.yml]
- [ ] [Review][Patch] Development dependencies (pytest, black, ruff) in production [environment.yml]
- [ ] [Review][Patch] Hardcoded environment name 'neuro_env' [Dockerfile]
- [ ] [Review][Patch] Container running as root [Dockerfile]
- [ ] [Review][Patch] Lack of checksum verification for Miniconda download [Dockerfile]
