# LLM Distillate: NeuroGemma Product Brief

## Meta-Context
- **Project:** NeuroGemma
- **Context:** Bachelor's Thesis Showcase Application
- **Input Source:** Brainstorming session (2026-05-09), Market research on Medical VLMs.

## Core Intent
Create a "Fast-Dev" Streamlit application to orchestrate and display results from 4 pre-developed AI models: 3 CNNs (Anatomical Plane, Sequence, Normalized Depth) and 1 fine-tuned MedGemma VLM.

## Strategic Innovation: The Axial-Flair Logic Gate
- **Logic:** CNNs classify image first. VLM (MedGemma) is triggered *only* if the scan is identified as Axial-Flair.
- **Value:** Dramatically reduces resource consumption (VRAM/Compute) and latency on the GPU server.

## Technical Architecture
- **Stack:** Monolithic Streamlit running on a GPU server.
- **Integration:** UI and Models run in the same Python environment to eliminate API complexity.
- **Model Wrapper:** Unified hub (`models.py`) with `@st.cache_resource` for efficient loading.
- **Defense Features:** Built-in "Mock Mode" and "Golden Dataset" for stable thesis presentations.

## UX & UI (The "Relieved" Philosophy)
- **Visuals:** Minimalist, "Medical Blue" accents, focused on reducing radiologist burnout.
- **Output:** Professional "Radiology Note" PDF.
- **PDF Fields:** Scan Image, Filename, Date, 3 CNN results (with confidence), and MedGemma Narrative.

## Success Criteria
1. Functional orchestration of all 4 models.
2. Flawless PDF report generation.
3. Stable demo performance via fallover modes.

## Out of Scope
- Model training/re-training.
- HIPAA/GDPR (using licensed/anonymized data).
- Persistent databases or auth.
