---
stepsCompleted: ["step-01-validate-prerequisites", "step-02-design-epics", "step-03-create-stories"]
inputDocuments: ["docs/_bmad_output/planning-artifacts/prd.md", "docs/_bmad_output/planning-artifacts/architecture.md", "docs/_bmad_output/planning-artifacts/ux-design-specification.md"]
---

# NeuroGemma - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for NeuroGemma, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR1: Users can upload a single medical brain scan image in common formats (JPG, PNG).
FR2: System can validate that the uploaded file is a supported image type before processing.
FR3: System can display the uploaded image clearly within the primary diagnostic interface.
FR4: System can execute an automated pipeline of four heterogeneous AI models (3 CNNs + 1 VLM).
FR5: System can classify the image based on Anatomical Plane (Axial, Sagittal, Coronal).
FR6: System can classify the image based on Sequence (T1, T2, FLAIR, etc.).
FR7: System can perform Normalized Depth Regression on the image.
FR8: System can conditionally trigger the MedGemma VLM narrative only when the CNNs confirm an "Axial-Flair" scan.
FR9: System can bypass VLM inference for non-Axial-Flair scans to optimize compute.
FR10: Users can view an integrated display of all model outputs (Plane, Sequence, Depth, and Narrative) on a single screen.
FR11: System can display the VLM narrative as raw, explainable text.
FR12: Users can see a real-time progress indicator as each stage of the orchestration pipeline executes.
FR13: System can display a clear "Diagnostic Status" (e.g., "Processing," "Complete," or "Skipped") for each model.
FR14: Users can generate a professional "Radiology Note" PDF with a single click.
FR15: System can synthesize the on-screen model findings and hidden metadata into the PDF report.
FR16: System can include the uploaded scan image in the generated PDF.
FR17: System can embed mandatory clinical disclaimers and human-in-the-loop validation notes into every PDF.
FR18: Users can toggle a "Mock Mode" to simulate successful pipeline execution without live model inference.
FR19: Users can access a dedicated "Technical Logs" view to verify the execution sequence of the Logic Gate.
FR20: System can provide clear error feedback if the pipeline fails or a model timeout occurs.
FR21: System can pre-load a "Golden Dataset" of curated images to ensure zero-latency retrieval during the thesis demonstration.
FR22: System can display visual "Confidence Indicators" (e.g., color-coded icons) alongside CNN labels to communicate model certainty.

### NonFunctional Requirements

NFR1: Initial 3-model CNN classification must complete within 30 seconds of image upload.
NFR2: MedGemma VLM narrative must be generated and displayed within 60 seconds of being triggered.
NFR3: PDF report must be ready for download within 10 seconds of clicking the generation button.
NFR4: All AI model execution must occur locally (no external cloud APIs).
NFR5: Application must not persist uploaded images or generated reports on disk beyond the active user session.
NFR6: "Mock Mode" must be architecturally decoupled from live model resources for 100% reliability.
NFR7: Monolithic server must maintain stable operation for at least 2 hours of continuous use.
NFR8: Interface must use high-contrast text and clinical color palette for legibility on 1080p projectors.
NFR9: Core diagnostic workflow must be minimalist and linear (minimal navigation/menus).
NFR10: All application components must be implemented in Python wherever feasible.
NFR11: Use ONNX Runtime for CNN inference and 4-bit quantization for MedGemma VLM.

### Additional Requirements

- **Starter Template:** Modern Modular Streamlit AI Template (src-layout).
- **Project Structure:** Decoupled monolith with `src/models`, `src/logic`, `src/reports`, and `src/utils`.
- **Infrastructure:** Docker with NVIDIA-container-toolkit and Python 3.12 (Conda).
- **State Management:** Centralized `InferenceState` class in `st.session_state` with structured logging (Decision Journal).
- **Reporting Engine:** Use `fpdf2` for professional "Radiology Note" PDF.
- **Privacy Policy:** Mandatory "Clear Session" trigger upon report download/privacy reset.
- **Latency Management:** Use "Pipeline Breadcrumbs" for transparency during inference.
- **Testing:** Pytest suite for Logic Gate and PDF synthesis.

### UX Design Requirements

UX-DR1: Implement "Relieved" aesthetic using minimalist "Medical Blue" palette, generous whitespace (2rem margins), and Bear-inspired clean typography (Inter/Open Sans).
UX-DR2: Two-Tab Dashboard layout: "Diagnostic View" (primary) vs. "Technical Logs" (secondary).
UX-DR3: Enhanced Image Upload Area with distinct drag-and-drop target and visual feedback states (Hover, Loading, Success).
UX-DR4: Pipeline Progress Indicator (Sequential "Breadcrumbs"): Low-saturation indicators (ID → Logic Gate → Synthesis → Report Ready).
UX-DR5: CNN Label Cards/Tags with label (e.g., "Axial") and confidence score (e.g., "[0.99]"), color-coded for certainty.
UX-DR6: Logic Gate Trigger Indicator: success-colored icon and "VLM Triggered" text when narrative is generated.
UX-DR7: Floating Action Button (FAB) for "Generate Report": circular/rounded persistent button at bottom-right.
UX-DR8: Technical Logs Viewer: Structured "Decision Journal" with timestamped model calls, outcomes, and logic gate decisions.
UX-DR9: Mock Mode Sidebar Toggle: Switch to instantly populate UI with "Golden Dataset" values.
UX-DR10: "Clear Session" trigger: Ensure report download wipes InferenceState for privacy.
UX-DR11: Contrast Ratio: Ensure "Medical Blue" and light gray backgrounds meet WCAG AA standards.
UX-DR12: Desktop-Only Focus: Optimized for 1080p workstations, not mobile-responsive.

### FR Coverage Map

FR1: Epic 2 - Users can upload a single medical brain scan image in common formats (JPG, PNG).
FR2: Epic 2 - System can validate that the uploaded file is a supported image type before processing.
FR3: Epic 3 - System can display the uploaded image clearly within the primary diagnostic interface.
FR4: Epic 2 - System can execute an automated pipeline of four heterogeneous AI models (3 CNNs + 1 VLM).
FR5: Epic 2 - System can classify the image based on Anatomical Plane (Axial, Sagittal, Coronal).
FR6: Epic 2 - System can classify the image based on Sequence (T1, T2, FLAIR, etc.).
FR7: Epic 2 - System can perform Normalized Depth Regression on the image.
FR8: Epic 2 - System can conditionally trigger the MedGemma VLM narrative only when the CNNs confirm an "Axial-Flair" scan.
FR9: Epic 2 - System can bypass VLM inference for non-Axial-Flair scans to optimize compute.
FR10: Epic 3 - Users can view an integrated display of all model outputs (Plane, Sequence, Depth, and Narrative) on a single screen.
FR11: Epic 3 - System can display the VLM narrative as raw, explainable text.
FR12: Epic 3 - Users can see a real-time progress indicator as each stage of the orchestration pipeline executes.
FR13: Epic 3 - System can display a clear "Diagnostic Status" (e.g., "Processing," "Complete," or "Skipped") for each model.
FR14: Epic 4 - Users can generate a professional "Radiology Note" PDF with a single click.
FR15: Epic 4 - System can synthesize the on-screen model findings and hidden metadata into the PDF report.
FR16: Epic 4 - System can include the uploaded scan image in the generated PDF.
FR17: Epic 4 - System can embed mandatory clinical disclaimers and human-in-the-loop validation notes into every PDF.
FR18: Epic 1 - Users can toggle a "Mock Mode" to simulate successful pipeline execution without live model inference.
FR19: Epic 4 - Users can access a dedicated "Technical Logs" view to verify the execution sequence of the Logic Gate.
FR20: Epic 3 - System can provide clear error feedback if the pipeline fails or a model timeout occurs.
FR21: Epic 1 - System can pre-load a "Golden Dataset" of curated images to ensure zero-latency retrieval during the thesis demonstration.
FR22: Epic 3 - System can display visual "Confidence Indicators" (e.g., color-coded icons) alongside CNN labels to communicate model certainty.

## Epic 1: Foundation & Demo Stability

Establish the "Modular Monolith" architecture, GPU-ready environment, and the Mock Mode fail-safe with "Golden Datasets" to ensure a robust foundation for development and demonstration.

**Goal:** A stable, containerized environment with a centralized state management system and a working "Mock Mode" for reliable demonstrations.

### Story 1.1: Project Initialization and Infrastructure Setup

As a Developer,
I want to initialize the project with a modular monolith structure and Docker configuration,
So that I have a consistent, GPU-ready environment for development and deployment.

**Acceptance Criteria:**

**Given** a new project directory
**When** I run the initialization process
**Then** the directory structure (src/models, src/logic, src/reports, src/utils) is created
**And** the Dockerfile and environment.yml (Conda) are configured with NVIDIA-container-toolkit support
**And** app.py is established as the Streamlit entry point.

### Story 1.2: Centralized State Management (InferenceState)

As a Developer,
I want to implement a centralized InferenceState class in st.session_state,
So that I can track model results, pipeline progress, and technical logs across the application session.

**Acceptance Criteria:**

**Given** a running Streamlit app
**When** the app initializes
**Then** a structured InferenceState object is created in st.session_state
**And** it includes fields for current_stage (Breadcrumbs), results (Model outputs), and step_logs (Decision Journal).

### Story 1.3: Mock Mode Engine and Golden Datasets

As a Developer,
I want to implement a "Mock Mode" engine that loads pre-defined "Golden Datasets,"
So that I can demonstrate the UI and reporting features even without access to live GPU resources.

**Acceptance Criteria:**

**Given** a toggle for "Mock Mode"
**When** I switch Mock Mode ON
**Then** the system loads static results from src/utils/mock_data.py
**And** live model inference is bypassed
**And** the InferenceState is populated with "Golden Dataset" values for Plane, Sequence, Depth, and Narrative.

### Story 1.4: Sidebar Controls and Privacy Reset

As a User,
I want a sidebar with a Mock Mode toggle and a "Clear Session" button,
So that I can control the demo stability and ensure my clinical data is wiped after each run.

**Acceptance Criteria:**

**Given** the Streamlit sidebar
**When** I toggle the Mock Mode switch
**Then** the application state immediately updates to reflect the mode change
**When** I click "Clear Session"
**Then** the InferenceState is reset to its initial empty state
**And** the UI reflects that no image or results are currently loaded.

## Epic 2: Intelligent Inference Engine (The Logic Gate)

Implement the core orchestration logic, including CNN wrappers (ONNX) and the conditional Axial-Flair Logic Gate to trigger the MedGemma VLM, ensuring compute efficiency and diagnostic accuracy.

**Goal:** A high-performance inference pipeline that intelligently coordinates multiple AI models based on scan classification.

### Story 2.1: Image Upload and Validation Logic

As a User,
I want the system to validate my uploaded brain scan image,
So that I only process supported file types (JPG, PNG) and receive clear feedback on errors.

**Acceptance Criteria:**

**Given** a file upload event
**When** the file is a JPG or PNG
**Then** the system accepts the file and prepares it for inference
**When** the file is an unsupported format or corrupted
**Then** the system blocks processing and provides an error message.

### Story 2.2: CNN Model Wrappers (ONNX)

As a Developer,
I want to implement independent wrappers for the three CNN models (Plane, Sequence, Depth) using ONNX Runtime,
So that I can perform high-speed quantitative classification on local hardware.

**Acceptance Criteria:**

**Given** an input image
**When** the CNN inference is triggered
**Then** the system classifies Anatomical Plane (Axial/Sagittal/Coronal), Sequence (T1/T2/FLAIR), and Depth
**And** each result includes a numerical confidence score
**And** the entire CNN stage completes within 30 seconds.

### Story 2.3: MedGemma VLM Wrapper (4-bit Quantized)

As a Developer,
I want to implement a wrapper for the MedGemma VLM using 4-bit quantization,
So that I can generate high-quality clinical narratives on local GPU memory.

**Acceptance Criteria:**

**Given** a triggered VLM inference request
**When** the model processes the image
**Then** it generates a raw natural language narrative
**And** the narrative generation completes within 60 seconds.

### Story 2.4: The Axial-Flair Logic Gate Orchestrator

As a Developer,
I want to implement the "Logic Gate" orchestration that conditionally triggers the VLM,
So that compute resources are only used for clinically relevant scans (Axial-Flair).

**Acceptance Criteria:**

**Given** the outputs from the 3 CNN models
**When** the CNNs confirm an "Axial" plane AND a "FLAIR" sequence
**Then** the system automatically triggers the MedGemma VLM
**When** the CNNs identify any other combination
**Then** the system bypasses the VLM and updates the InferenceState to reflect a "Skipped" narrative status.

### Story 2.5: Integrated Inference Pipeline with State Logging

As a Developer,
I want an integrated run_pipeline function that updates the InferenceState at every stage,
So that the UI and Technical Logs have access to real-time execution data.

**Acceptance Criteria:**

**Given** a validated image
**When** the pipeline starts
**Then** InferenceState.current_stage is updated as it moves through ID, GATE, and SYNTHESIS
**And** every model call (success or skip) is appended to step_logs in the standardized dictionary format.

## Epic 3: "Relieved" Clinical Dashboard

Build the primary Streamlit interface using the "Medical Blue" aesthetic, featuring the two-tab layout, real-time pipeline breadcrumbs, and a unified display for synthesized model outputs.

**Goal:** A minimalist, professional clinical interface that reduces cognitive load and provides transparent progress feedback.

### Story 3.1: "Relieved" Aesthetic and Two-Tab Layout

As a User,
I want a minimalist "Medical Blue" interface with a Two-Tab layout,
So that I can focus on my diagnosis in a calm environment while still having access to technical logs.

**Acceptance Criteria:**

**Given** the app.py entry point
**When** I load the application
**Then** the "Medical Blue" color palette and "Relieved" spacing (2rem margins) are applied via custom CSS
**And** the UI is divided into two tabs: "Diagnostic View" and "Technical Logs"
**And** the interface is optimized for a 1080p desktop workstation.

### Story 3.2: Enhanced Image Upload Area with Feedback

As a User,
I want an intuitive drag-and-drop area for uploading my brain scans,
So that I can easily initiate the inference process with clear visual feedback.

**Acceptance Criteria:**

**Given** the "Diagnostic View" tab
**When** I view the upload area
**Then** it displays a clear drag-and-drop target with instruction text
**And** it provides visual feedback for different states: Hover, Loading, and Success (showing the uploaded image).

### Story 3.3: Pipeline Progress Indicator (Breadcrumbs)

As a User,
I want to see sequential "Pipeline Breadcrumbs" during inference,
So that I understand the system's progress during the 60-second latency period.

**Acceptance Criteria:**

**Given** an active inference pipeline
**When** a stage (ID, GATE, SYNTHESIS) is executing
**Then** the corresponding breadcrumb in the UI lights up with a low-saturation indicator
**And** the status updates in real-time based on InferenceState.current_stage.

### Story 3.4: Unified Diagnostic Results Display

As a User,
I want to see all model outputs (labels, tags, and narrative) in a single horizontal layout,
So that I can synthesize the diagnostic findings effortlessly.

**Acceptance Criteria:**

**Given** completed inference results
**When** I view the "Diagnostic View"
**Then** the CNN labels (Plane, Sequence, Depth) are displayed as color-coded cards with confidence scores
**And** the MedGemma VLM narrative is displayed as clear, explainable text
**And** if the VLM was triggered, a success-colored "VLM Triggered" indicator is shown.

### Story 3.5: Error Handling and Diagnostic Status

As a User,
I want to see clear status indicators and error messages for each stage,
So that I know if a model was skipped or if a failure occurred.

**Acceptance Criteria:**

**Given** the results display
**When** a model completes, fails, or is skipped
**Then** the UI displays a clear "Diagnostic Status" (e.g., "Complete," "Skipped," or "Error")
**And** if a pipeline failure or timeout occurs, human-readable error feedback is provided.

## Epic 4: Synthesized Reporting & Audit Trail

Finalize the "Radiology Note" PDF engine and the technical "Decision Journal," enabling professional documentation and transparent evidence of the AI's orchestration logic.

**Goal:** Professional clinical documentation and transparent technical auditing.

### Story 4.1: Professional "Radiology Note" PDF Engine

As a User,
I want to generate a professional PDF "Radiology Note" with a single click,
So that I can document the synthesized findings in a standard clinical format.

**Acceptance Criteria:**

**Given** completed inference results
**When** I click the "Generate Report" button
**Then** the system uses fpdf2 to synthesize the findings (CNN labels + VLM narrative) into a PDF
**And** the PDF includes the uploaded scan image
**And** the PDF includes the mandatory clinical disclaimer and human-in-the-loop validation notes
**And** the report is ready for download within 10 seconds.

### Story 4.2: Floating Action Button (FAB) for PDF Export

As a User,
I want a persistent "Generate Report" button that is easy to find after inference,
So that I can quickly transition from diagnosis to documentation.

**Acceptance Criteria:**

**Given** the "Diagnostic View"
**When** the inference pipeline is complete
**Then** a circular/rounded Floating Action Button (FAB) appears at the bottom-right of the screen
**And** clicking it triggers the PDF generation process.

### Story 4.3: Technical "Decision Journal" (Logs Viewer)

As a Thesis Evaluator,
I want to see a structured "Decision Journal" of the AI's orchestration logic,
So that I can verify the engineering integrity and Logic Gate decisions.

**Acceptance Criteria:**

**Given** the "Technical Logs" tab
**When** I view the logs
**Then** it displays a structured, timestamped audit trail from InferenceState.step_logs
**And** it clearly shows which models were triggered, which were bypassed, and their corresponding confidence scores.

### Story 4.4: Automatic Session Reset on Report Download

As a User,
I want my session data to be automatically wiped after I download my report,
So that I can ensure patient privacy and prevent state leakage between different scans.

**Acceptance Criteria:**

**Given** a successful report generation and download
**When** the download is completed or the action is triggered
**Then** the InferenceState is automatically reset (equivalent to a "Clear Session" action)
**And** the UI returns to its initial upload state.





