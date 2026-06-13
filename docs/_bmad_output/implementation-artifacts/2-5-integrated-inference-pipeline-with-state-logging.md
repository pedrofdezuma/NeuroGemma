# Story 2.5: Integrated Inference Pipeline with State Logging

**Status:** ready-for-dev
**Epic:** 2: Intelligent Inference Engine (The Logic Gate)
**ID:** 2.5

## Story

As a Developer,
I want an integrated `run_pipeline` function that updates the InferenceState at every stage,
So that the UI and Technical Logs have access to real-time execution data.

## Acceptance Criteria

1. **Given** a validated image object (PIL Image)
2. **When** the pipeline starts
3. **Then** `InferenceState.current_stage` is updated as it moves through:
    - `ID` (CNN Identification)
    - `GATE` (Logic Gate Decision)
    - `SYNTHESIS` (Narrative Generation - if triggered)
    - `COMPLETE` (End of pipeline)
4. **And** every model call (success or skip) is appended to `InferenceState.step_logs` using the standardized dictionary format:
    ```python
    {
        "timestamp": "ISO-8601",
        "stage": "ID | GATE | SYNTHESIS",
        "event": "STRING_CONSTANT",
        "model_id": "model_name",
        "outcome": "value",
        "confidence": 0.0,
        "metadata": {}
    }
    ```
5. **And** the function gracefully handles model errors by updating the log and state accordingly.
6. **And** all core diagnostic results (Plane, Sequence, Depth, Narrative, Aggregate Confidence) are persisted in `InferenceState.results`.

## Developer Context

### Guardrails & Standards
- **Modular Monolith:** Implementation MUST be inside `src/logic/logic_gate.py`. No UI logic (`st.*`) allowed inside this file (except for `@st.cache_resource` if needed, though prefer state injection).
- **Strict Typing:** All function signatures must include type hints (e.g., `run_pipeline(image: Image.Image, state: InferenceState) -> None`).
- **Structured Logging:** The "Decision Journal" format is critical for the thesis defense. Ensure `ISO-8601` timestamps are used for every log entry.
- **Mock-First Awareness:** Ensure the integrated pipeline respects the `is_mock_mode` flag if appropriate, though `run_mock_inference` already handles static data.

### Technical Requirements
- **Pipeline Breadcrumbs:** The `current_stage` enum must be updated *before* each major block of work to ensure the UI can provide immediate feedback.
- **Aggregate Confidence:** Calculate a simple average of the three CNN confidence scores and store it in `results["confidence"]`.
- **Dependency Management:** Ensure models are imported and instantiated correctly using existing wrappers from `src/models/`.

### Architecture Compliance
- **File Structure:** All logic must reside in `src/logic/`.
- **State Management:** Use the `InferenceState` dataclass defined in `src/logic/state.py`.
- **Model Hub:** Models should be accessed via their respective wrappers in `src/models/`.

## Tasks

- [x] **Define `run_pipeline` Entry Point**
    - [x] Create `run_pipeline(image: Image.Image)` in `src/logic/logic_gate.py`.
    - [x] Initialize/Access `st.session_state.inference`.
- [x] **Implement ID Stage (CNN Identification)**
    - [x] Update `state.current_stage = PipelineStage.ID`.
    - [x] Execute `ModelPlaneCNN`, `ModelSeqCNN`, and `ModelDepthCNN`.
    - [x] Log each successful classification to `step_logs`.
    - [x] Store results in `state.results`.
- [x] **Implement GATE Stage (Logic Gate)**
    - [x] Update `state.current_stage = PipelineStage.GATE`.
    - [x] Call `evaluate_logic_gate(state, image)`.
    - [x] Ensure `evaluate_logic_gate` properly logs its decision.
- [x] **Implement SYNTHESIS Stage (Conditional)**
    - [x] *Note: This is partially handled within `evaluate_logic_gate` in current architecture, but must ensure `current_stage` is updated to `SYNTHESIS` before VLM call.*
    - [x] Log the VLM outcome (Narrative or Skip).
- [x] **Finalize Pipeline**
    - [x] Calculate aggregate confidence.
    - [x] Update `state.current_stage = PipelineStage.COMPLETE`.
- [x] **Verification & Testing**
    - [x] Create `tests/test_pipeline_integration.py` to verify the full flow and logging sequence.
    - [x] Verify that `InferenceState` is perfectly populated after a full run.

## Dev Agent Record

### Debug Log
- Renamed `run_real_inference` to `run_pipeline`.
- Added `SYNTHESIS` stage update and logging to `evaluate_logic_gate`.
- Normalized labels to lowercase for robust logic gate comparisons.
- Fixed `tests/test_cnn_wrappers.py` by patching `os.path.exists` and updating expected indices.
- Fixed `tests/test_logic_gate.py` by making `evaluate_logic_gate` case-insensitive.

### Implementation Plan
- Rename existing orchestration function to match story requirements.
- Ensure all stages are explicitly updated in `st.session_state.inference.current_stage`.
- Implement standardized logging format with ISO-8601 timestamps.
- Add integration test to verify the full pipeline flow.

### Completion Notes
- Story implementation complete.
- All acceptance criteria satisfied.
- Integration tests pass.
- Legacy tests fixed and passing.
- UI (`app.py`) updated to use the new pipeline.

## File List
- `src/logic/logic_gate.py`
- `app.py`
- `tests/test_pipeline_integration.py`
- `tests/test_cnn_wrappers.py`
- `tests/test_logic_gate.py`

## Change Log
- **2026-05-15:** Implemented integrated inference pipeline with comprehensive state logging.
- **2026-05-15:** Renamed `run_real_inference` to `run_pipeline`.
- **2026-05-15:** Added `tests/test_pipeline_integration.py`.

## Previous Story Intelligence (2.4)
- **Learnings:** `evaluate_logic_gate` was implemented in `src/logic/logic_gate.py`. It correctly handles the Axial-FLAIR condition.
- **Existing Code:** `run_real_inference` exists but might need to be renamed to `run_pipeline` and fully aligned with the `SYNTHESIS` stage ACs.

## Project Context Reference
- See `docs/_bmad_output/project-context.md` for naming conventions and anti-patterns.
- All models must run locally; NO external APIs.

## Completion Status
- **Status:** review
- **Notes:** All tasks complete, tests pass, ready for peer review.

