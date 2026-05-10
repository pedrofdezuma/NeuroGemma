---
stepsCompleted: ["step-01-init", "step-02-discovery", "step-02b-vision", "step-02c-executive-summary", "step-03-success", "step-04-journeys", "step-05-domain", "step-06-innovation", "step-07-project-type", "step-08-scoping", "step-09-functional", "step-10-nonfunctional", "step-11-polish"]
inputDocuments: ["product-brief-NeuroGemma.md", "brainstorming-session-2026-05-09-13-35-50.md", "distillate-NeuroGemma.md"]
documentCounts:
  briefCount: 1
  researchCount: 1
  brainstormingCount: 1
  projectDocsCount: 0
workflowType: 'prd'
releaseMode: phased
classification:
  projectType: Web App (Streamlit)
  domain: Healthcare (Medical AI/Radiology)
  complexity: High
  projectContext: greenfield
---

# Product Requirements Document - NeuroGemma

**Author:** Pedro
**Date:** 2026-05-10

## Executive Summary

NeuroGemma is a high-performance orchestration and visualization platform designed to bridge the "deployment gap" in medical AI. It transforms fragmented outputs from multiple specialized models into a single, cohesive clinical interface. By integrating three pre-developed CNNs (Anatomical Plane, Sequence, Normalized Depth) and a fine-tuned MedGemma VLM, the application provides radiologists with a unified diagnostic workflow. The primary goal is to demonstrate that a sophisticated, multi-source AI system can be both compute-efficient and hospital-ready, moving beyond isolated research models to a functional clinical tool.

### What Makes This Special

*   **Unified Diagnostic Insight:** NeuroGemma eliminates "inference fatigue" by consolidating results from four distinct AI sources into a single screen, removing the need for clinicians to manually synthesize data from disparate outputs.
*   **The Axial-Flair Logic Gate:** A strategic orchestration layer that uses CNN classifications to conditionally trigger the MedGemma VLM. This ensures high-performance output while maintaining compute efficiency on accessible hardware.
*   **"Relieved" UX Philosophy:** Unlike data-heavy research tools, the interface is designed to reduce cognitive load, featuring a minimalist "Medical Blue" aesthetic and generating a professional, one-click "Radiology Note" PDF.

## Project Classification

*   **Project Type:** Web App (Monolithic Streamlit)
*   **Domain:** Healthcare (Medical AI / Radiology)
*   **Complexity:** High (Multi-model orchestration, clinical requirements)
*   **Project Context:** Greenfield (Bachelor’s Thesis Showcase)

## Success Criteria

### User Success
*   **Execution Robustness:** 100% successful execution of the full pipeline (Upload → Inference → UI Display → PDF) during the thesis defense.
*   **Orchestration Accuracy:** The "Axial-Flair Logic Gate" correctly triggers the VLM narrative for all relevant scans in the "Golden Dataset" without manual intervention.
*   **Reporting Fidelity:** Successful generation of a professional "Radiology Note" PDF that accurately reflects the on-screen model outputs for every run.

### Technical Success
*   **Orchestration Integrity:** Zero-leakage compute; the VLM is never invoked unless the CNN classifiers confirm an Axial-Flair scan.
*   **Demo Stability:** Availability of a "Mock Mode" that provides a 100% reliable simulation of the application’s UI and PDF generation, independent of GPU server or network status.
*   **Modular Monolith Architecture:** Successful implementation of a unified `models.py` hub using `@st.cache_resource` for efficient model management.

### Measurable Outcomes
*   **Pipeline Reliability:** 0% crash rate during the live demonstration.
*   **Logic Accuracy:** 100% adherence to the "Axial-Flair Logic Gate" conditional rules.

## Product Scope

### MVP - Minimum Viable Product (Thesis Defense)
*   **Single Image Upload:** Support for standard image formats (JPG/PNG).
*   **4-Model Orchestration:** Integrated hub for 3 CNNs and 1 MedGemma VLM.
*   **Axial-Flair Logic Gate:** Automated conditional inference pipeline.
*   **Diagnostic UI:** "Relieved" minimalist interface using Medical Blue accents.
*   **Report Engine:** One-click generation of the "Radiology Note" PDF.
*   **Mock Mode:** Built-in demo stability toggle.

### Vision (Future / Out of Scope)
*   **Hospital System Integration:** Connection to HIS/PACS environments.
*   **3D Volumetric Rendering:** Processing of full 3D scan volumes.
*   **Batch Processing:** Support for multi-image or study-level uploads.
*   **User Authentication:** Secure login and multi-user management.
*   **DICOM Support:** Native handling of medical-standard DICOM metadata.

## User Journeys

### 1. The Expert's "Relieved" Workflow
**Persona:** Dr. Elena, a senior radiologist managing high daily scan volumes.
*   **Narrative:** Dr. Elena starts her shift with a large backlog of brain scans. She seeks a tool that reduces her cognitive load rather than adding to it. She opens NeuroGemma’s minimalist interface and uploads a T2-FLAIR axial image. 
*   **The Moment of Value:** Instead of navigating multiple windows, she sees the CNN results (Plane, Sequence, Depth) and the MedGemma VLM narrative side-by-side on a single screen. 
*   **Resolution:** With one click, she generates a professional "Radiology Note" PDF. She feels "relieved" by the automated synthesis of complex AI data into a standard report format.

### 2. The Thesis Defense "Golden Path"
**Persona:** Pedro, the student, demonstrating the project to his thesis committee.
*   **Narrative:** Pedro needs to prove the intelligence of the "Axial-Flair Logic Gate." He first uploads a Sagittal T1 scan. The system correctly identifies it and visibly bypasses the VLM, saving compute resources. 
*   **The Moment of Value:** He then uploads a "Golden Dataset" Axial-Flair image. The Logic Gate instantly triggers the MedGemma VLM, displaying its complex narrative reasoning.
*   **Resolution:** The committee observes the orchestration working flawlessly, validating the architectural efficiency and the project’s core technical innovation.

### 3. The "Network Failure" Recovery
**Persona:** Pedro, ensuring a stable demonstration during high-pressure moments.
*   **Narrative:** During the live defense, the GPU research server experiences a connection hiccup. Pedro remains calm and toggles the "Mock Mode" switch on the dashboard.
*   **The Moment of Value:** He "uploads" an image, and the interface instantly populates with pre-loaded mock data and generates a perfect PDF report.
*   **Resolution:** The presentation continues without interruption, proving "Demo Stability" and high-quality defensive engineering to the examiners.

### Journey Requirements Summary
*   **Diagnostic Dashboard:** A single-view UI for multi-model output display.
*   **Conditional Pipeline Engine:** Backend logic for the "Axial-Flair Logic Gate."
*   **Stability Toggle:** A persistent UI control for "Mock Mode" failover.
*   **Report Generator:** A PDF engine that synthesizes on-screen and hidden model metadata.
*   **File Handling:** Robust error handling for non-brain or unsupported file types.

## Domain-Specific Requirements

### Compliance & Regulatory
*   **Data Privacy:** The application exclusively processes images from anonymized research datasets. No Personally Identifiable Information (PII) is stored or processed.
*   **Legal Disclaimer:** A mandatory "For Research and Educational Use Only" disclaimer must be displayed in the application footer and at the bottom of every generated "Radiology Note" PDF.
*   **Human-in-the-Loop:** Every generated PDF report includes a note stating that the content is a **preliminary draft generated by AI** and requires review and validation by a qualified clinical expert.

### Technical Constraints (Safety & Security)
*   **Data Sovereignty:** All AI inference (CNN and VLM) is performed locally on the host GPU server. No patient data or model inputs are transmitted to external APIs or third-party cloud services.
*   **Explainable Output:** To maintain academic transparency, the MedGemma VLM narrative is displayed as **raw text**, allowing the expert to evaluate the model's direct reasoning without post-processing distortion.

### Risk Mitigations
*   **Hallucination Prevention (Logic Gate):** The "Axial-Flair Logic Gate" acts as the primary safety mechanism. It prevents VLM inference on out-of-distribution (non-axial or non-flair) images, significantly reducing the risk of model hallucinations.
*   **Inference Guardrails:** The system uses 3-model CNN classification to validate image type before any qualitative analysis (VLM) is initiated.

## Innovation & Novel Patterns

### Detected Innovation Areas
*   **Multi-Model Orchestration:** The "Axial-Flair Logic Gate" is a novel architectural pattern for thesis-level projects. It coordinates four heterogeneous AI models (CNNs and VLMs) into a unified inference pipeline, ensuring that compute-heavy resources are only used when clinically relevant.
*   **Generative Clinical Reasoning:** Unlike standard diagnostic tools that provide simple labels, NeuroGemma leverages a fine-tuned MedGemma VLM to provide natural language narratives, demonstrating the potential for LLMs to act as automated reporting assistants.
*   **"Relieved" UX Design:** A specialized minimalist aesthetic that addresses "clinician burnout" by simplifying complex multi-model data into a single, cohesive, and soothing interface.

### Market Context & Competitive Landscape
*   **Closing the Deployment Gap:** While medical AI research often focuses on individual model accuracy, NeuroGemma innovates at the **integration layer**, showing how a monolithic server can bridge the gap between raw research models and a hospital-ready tool.
*   **Compute Efficiency:** The project challenges the assumption that advanced VLM inference requires excessive cloud resources, proving that local, logic-gated execution on accessible hardware is viable for clinical showcases.

### Validation Approach
*   **Pipeline Visibility:** The application includes a "Debug/Pipeline Log" view (separate from the main diagnostic UI) to provide technical evidence of the Logic Gate's execution sequence and model trigger status.
*   **Inference Accuracy:** 100% visual validation that all 4 model fields (Plane, Sequence, Depth, and Narrative) are populated correctly during the live demonstration.

### Risk Mitigation
*   **The Orchestration Safety Valve:** The system mitigates VLM "hallucination" risk by using the CNN classifiers as a primary filter, ensuring the VLM only processes images within its specialized domain (Axial-Flair).
*   **Fail-Safe Mode:** The built-in "Mock Mode" ensures that the innovative UI and PDF features can still be demonstrated even if the underlying GPU hardware is unavailable.

## Project Scoping & Phased Development

### MVP Strategy & Philosophy
*   **MVP Approach:** Showcase MVP. The goal is to provide a functional proof-of-concept that validates the orchestration of four heterogeneous AI models into a unified clinical interface.
*   **Resource Requirements:** Single developer (Bachelor's Thesis) using a Streamlit/Python stack on a dedicated GPU research server.

### MVP Feature Set (Phase 1: Thesis Defense)
**Core User Journeys Supported:**
*   The Expert's "Relieved" Workflow (Unified diagnostic insight).
*   The Thesis Defense "Golden Path" (Logic Gate validation).
*   The "Network Failure" Recovery (Demo stability).

**Must-Have Capabilities:**
*   **Integrated Model Hub:** Local loading of 3 CNNs and 1 fine-tuned VLM.
*   **Axial-Flair Logic Gate:** Automated conditional inference pipeline.
*   **Two-Tab Dashboard:** Clean "Diagnostic View" vs. detailed "Technical Logs."
*   **Progress Visualization:** Real-time pipeline status indicators.
*   **Report Engine:** One-click "Radiology Note" PDF generation with clinical disclaimer.
*   **Failover System:** Built-in "Mock Mode" for high-stakes demonstration stability.

### Post-MVP Features (Future Vision)
*   **Phase 2 (Scalability):** Support for Batch Uploads and multi-study processing.
*   **Phase 3 (Expansion):** User Authentication, HIS/PACS integration, and DICOM metadata handling.

### Risk Mitigation Strategy
*   **Technical Risks (Orchestration):** The risk of the app failing to trigger the correct model sequence. **Mitigation:** Comprehensive pipeline logs in the "Technical Logs" tab to verify internal logic.
*   **Technical Risks (Stability):** The risk of server/network failure during a live demo. **Mitigation:** The "Mock Mode" fail-safe allows for a 100% reliable simulation of the UI and PDF features.
*   **Resource Risks:** Complexity of VLM integration on local hardware. **Mitigation:** Modular Monolith approach (Streamlit) to minimize API overhead and development time.

## Web App Specific Requirements

### Project-Type Overview
*   **Architecture:** Monolithic Streamlit Application (SPA) running on a local/on-premise GPU server.
*   **UX Structure:** A "Two-Tab" layout designed to separate the clinical diagnostic experience from technical engineering evidence.

### Technical Architecture Considerations
*   **Diagnostic Tab (Primary):** A "Relieved" minimalist view containing only the image uploader, the integrated model results (3 CNNs + 1 VLM), and the PDF generation button.
*   **Technical Logs Tab (Secondary):** A dedicated view for pipeline logs, showing the "Axial-Flair Logic Gate" execution sequence and model-trigger status for technical evaluation.
*   **State Management:** Utilization of `st.session_state` to handle the multi-model pipeline data without a persistent database.
*   **Performance Cache:** Implementation of `@st.cache_resource` for the unified Model Hub (`models.py`) to ensure zero-latency model reloading.

### Implementation Considerations
*   **Progress Feedback:** Integrated real-time progress indicators (e.g., `st.status`) to visualize the orchestration pipeline status as models are triggered or bypassed.
*   **Browser Matrix:** Optimized for modern desktop browsers (Chrome, Edge, Safari) at standard 1080p laptop resolutions.
*   **Responsive Layout:** Fixed-width centered layout to simulate a professional clinical workstation tool.

## Functional Requirements

### Image Management & Input
*   **FR1:** Users can upload a single medical brain scan image in common formats (JPG, PNG).
*   **FR2:** System can validate that the uploaded file is a supported image type before processing.
*   **FR3:** System can display the uploaded image clearly within the primary diagnostic interface.

### Model Orchestration (The Logic Gate)
*   **FR4:** System can execute an automated pipeline of four heterogeneous AI models (3 CNNs + 1 VLM).
*   **FR5:** System can classify the image based on Anatomical Plane (Axial, Sagittal, Coronal).
*   **FR6:** System can classify the image based on Sequence (T1, T2, FLAIR, etc.).
*   **FR7:** System can perform Normalized Depth Regression on the image.
*   **FR8:** System can conditionally trigger the MedGemma VLM narrative *only* when the CNNs confirm an "Axial-Flair" scan.
*   **FR9:** System can bypass VLM inference for non-Axial-Flair scans to optimize compute.

### Diagnostic Visualization (Relieved UX)
*   **FR10:** Users can view an integrated display of all model outputs (Plane, Sequence, Depth, and Narrative) on a single screen.
*   **FR11:** System can display the VLM narrative as raw, explainable text.
*   **FR12:** Users can see a real-time progress indicator as each stage of the orchestration pipeline executes.
*   **FR13:** System can display a clear "Diagnostic Status" (e.g., "Processing," "Complete," or "Skipped") for each model.
*   **FR22:** System can display visual "Confidence Indicators" (e.g., color-coded icons) alongside CNN labels to communicate model certainty.

### Reporting & Documentation
*   **FR14:** Users can generate a professional "Radiology Note" PDF with a single click.
*   **FR15:** System can synthesize the on-screen model findings and hidden metadata into the PDF report.
*   **FR16:** System can include the uploaded scan image in the generated PDF.
*   **FR17:** System can embed mandatory clinical disclaimers and human-in-the-loop validation notes into every PDF.

### Technical & Defensive Engineering
*   **FR18:** Users can toggle a "Mock Mode" to simulate successful pipeline execution without live model inference.
*   **FR19:** Users can access a dedicated "Technical Logs" view to verify the execution sequence of the Logic Gate.
*   **FR20:** System can provide clear error feedback if the pipeline fails or a model timeout occurs.
*   **FR21:** System can pre-load a "Golden Dataset" of curated images to ensure zero-latency retrieval during the thesis demonstration.

## Non-Functional Requirements

### Performance
*   **NFR1:** The system must complete the initial 3-model CNN classification (Plane, Sequence, Depth) within **30 seconds** of image upload.
*   **NFR2:** The MedGemma VLM narrative must be generated and displayed within **60 seconds** of being triggered by the Logic Gate.
*   **NFR3:** The "Radiology Note" PDF must be synthesized and ready for user download within **10 seconds** of clicking the generation button.

### Security & Privacy
*   **NFR4:** All AI model execution (CNN and VLM) must occur locally on the application host. No data may be transmitted to external cloud services or APIs.
*   **NFR5:** To protect patient privacy, the application must not persist uploaded images or generated reports on disk beyond the duration of the active user session.

### Reliability (Demo Stability)
*   **NFR6:** The "Mock Mode" must be architecturally decoupled from live model resources, ensuring a 100% reliable simulation even in the event of hardware or server failure.
*   **NFR7:** The monolithic server must maintain stable operation for at least **2 hours of continuous use** without requiring a service restart.

### Accessibility & UX Quality
*   **NFR8:** The interface must use high-contrast text and a consistent clinical color palette to ensure legibility on standard high-definition projectors (1080p).
*   **NFR9:** The core diagnostic workflow must be minimalist and linear, ensuring users can reach the PDF generation stage without navigating complex menus.

### Implementation Constraints
*   **NFR10:** All application components—including the diagnostic UI, model orchestration pipeline, and report generation engine—must be implemented in **Python** wherever feasible to ensure seamless integration with the AI research stack.
*   **NFR11:** The application must utilize **ONNX Runtime** for CNN inference and **4-bit quantization** for the MedGemma VLM to ensure high performance on local hardware.
