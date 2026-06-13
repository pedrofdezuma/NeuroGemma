# Story 2.4: The Axial-Flair Logic Gate Orchestrator

Status: review

## Story

As a Developer,
I want to implement the "Logic Gate" orchestration that conditionally triggers the VLM,
so that compute resources are only used for clinically relevant scans (Axial-Flair).

## Acceptance Criteria

1. **Given** the outputs from the 3 CNN models (Plane, Sequence, Depth)
2. **When** the CNNs confirm an "Axial" plane AND a "FLAIR" sequence
3. **Then** the system automatically triggers the MedGemma VLM inference
4. **When** the CNNs identify any other combination
5. **Then** the system bypasses the VLM and updates the `InferenceState` to reflect a "Analysis Skipped (Scan not Axial-FLAIR)" narrative status
6. **And** the logic is implemented within `src/logic/logic_gate.py`
7. **And** every decision point (Trigger vs. Skip) is appended to `InferenceState.step_logs` using the standardized dictionary format

## Tasks / Subtasks

- [x] **Implement Logic Gate Orchestration** (AC: #1, #2, #3, #4, #5, #6)
  - [x] Implement `evaluate_logic_gate(inference_state: InferenceState, image: Image.Image)` in `src/logic/logic_gate.py`
  - [x] Implement conditional logic: `if plane == "Axial" and sequence == "FLAIR"`
  - [x] If True: Instantiate `ModelMedGemmaVLM` and call `predict(image)`
  - [x] If False: Set `inference_state.results["narrative"] = "Analysis Skipped (Scan not Axial-FLAIR)"`
- [x] **Implement Structured Logging** (AC: #7)
  - [x] Log the GATE decision to `inference_state.step_logs`
  - [x] Use standardized format: `{"timestamp": "...", "stage": "GATE", "event": "GATE_DECISION", "model_id": "logic_gate", "outcome": "TRIGGERED" | "SKIPPED", ...}`
- [x] **Author Comprehensive Tests** (AC: #1, #2, #4)
  - [x] Update `tests/test_logic_gate.py`
  - [x] Create test cases for both Triggered and Skipped paths
  - [x] Mock CNN results and VLM wrapper to isolate logic gate testing

## Dev Notes

- **Architecture Boundary:** `src/logic/` should not import `streamlit` except for `st.cache_resource` or session state access if strictly necessary, but prefer passing the state object.
- **Pattern:** Follow the "Decision Journal" format for logs as defined in `architecture.md`.
- **VLM Trigger:** Ensure the VLM is only loaded and called if the gate condition is met to save memory.
- **State Integration:** The results must be stored in `inference_state.results["narrative"]`.

### Project Structure Notes

- **File Path:** `src/logic/logic_gate.py`
- **Dependency:** Requires `ModelMedGemmaVLM` from `src/models/model_medgemma_vlm.py`.
- **Dependency:** Requires `InferenceState` from `src/logic/state.py`.

### References

- **Architecture:** `docs/_bmad_output/planning-artifacts/architecture.md#Decision Journal`
- **Architecture:** `docs/_bmad_output/planning-artifacts/architecture.md#Logic Boundary`
- **Epics:** `docs/_bmad_output/planning-artifacts/epics.md#Story 2.4: The Axial-Flair Logic Gate Orchestrator`
- **UX Spec:** `docs/_bmad_output/planning-artifacts/ux-design-specification.md#3.1 The Diagnostic Synthesis`

## Dev Agent Record

### Agent Model Used

Gemini 1.5 Pro (via Gemini CLI)

### Debug Log References

- Logic Gate decision correctly logged with ISO-8601 timestamp.
- VLM triggered only on Axial-FLAIR.
- Skipped status correctly updated in `InferenceState`.

### Completion Notes List

- Implemented `evaluate_logic_gate` in `src/logic/logic_gate.py`.
- Added unit tests in `tests/test_logic_gate.py` covering both success and bypass paths.
- Verified compliance with Decision Journal logging format.

### File List
- src/logic/logic_gate.py
- tests/test_logic_gate.py

## Change Log

- **2026-05-15**: Implemented Logic Gate orchestration and structured logging. Added unit tests for Triggered and Skipped paths. (Dev Agent: Gemini CLI)


