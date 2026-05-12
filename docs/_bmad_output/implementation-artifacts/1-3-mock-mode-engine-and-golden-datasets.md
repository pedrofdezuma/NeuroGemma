# Story 1.3: Mock Mode Engine and Golden Datasets

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Developer,
I want to implement a "Mock Mode" engine that loads pre-defined "Golden Datasets,"
so that I can demonstrate the UI and reporting features even without access to live GPU resources.

## Acceptance Criteria

1. **Toggle Integration:** When "Mock Mode" is switched ON in the sidebar, live inference is bypassed (to be fully integrated when models are added).
2. **Mock Data Engine:** The system loads static results from a new utility file `src/utils/mock_data.py`.
3. **Golden Dataset Coverage:** The engine provides pre-defined results for at least two scenarios:
    - **Scenario A (Axial-Flair):** Triggers VLM narrative.
    - **Scenario B (Sagittal T1):** Bypasses VLM narrative.
4. **State Population:** The `InferenceState` is correctly populated with mock values:
    - `results`: Plane, Sequence, Depth, Narrative, and numerical confidence scores.
    - `current_stage`: Set to `PipelineStage.COMPLETE`.
5. **Decision Journal Simulation:** The `step_logs` in `InferenceState` are populated with realistic mock entries mirroring the logical pipeline stages (ID -> GATE -> SYNTHESIS).
6. **Zero-Latency Simulation:** Mock results should appear instantly (or with a small simulated delay of <1s) to facilitate rapid UI testing.

## Tasks / Subtasks

- [x] **Create Mock Data Utility** (AC: #2, #3)
  - [x] Create `src/utils/mock_data.py`
  - [x] Define `GOLDEN_DATASETS` dictionary with at least two MRI scan scenarios.
  - [x] Implement `get_mock_results(dataset_id: str) -> dict` helper.
- [x] **Implement Mock Orchestration Logic** (AC: #1, #4, #5)
  - [x] Create `src/logic/logic_gate.py` (if not exists)
  - [x] Implement `run_mock_inference(dataset_id: str)` function that:
    - [x] Clears existing results.
    - [x] Populates `st.session_state.inference.results` from mock data.
    - [x] Appends simulated entries to `st.session_state.inference.step_logs`.
    - [x] Updates `st.session_state.inference.current_stage` to `COMPLETE`.
- [x] **Integrate with UI** (AC: #1)
  - [x] Update `app.py` to show a "Load Golden Dataset" selection when Mock Mode is ON.
  - [x] Trigger `run_mock_inference` upon selection or a mock "Process" button.
- [x] **Validation & Testing**
  - [x] Create `tests/test_mock_data.py` to verify data retrieval.
  - [x] Verify that UI correctly displays mock results and logs.

## Dev Notes

### Architecture & Standards
- **Modular Monolith:** Mock data definitions belong in `src/utils/`, while the logic to populate state belongs in `src/logic/`. [Source: `architecture.md#Unified Structure`]
- **Strict Typing:** All new functions must use type hints.
- **Decision Journal Format:** Ensure mock logs follow the schema established in Story 1.2:
  ```python
  {
      "timestamp": "ISO-8601",
      "stage": "ID | GATE | SYNTHESIS | COMPLETE",
      "event": "STRING_CONSTANT",
      "model_id": "model_name",
      "outcome": "value",
      "confidence": 0.0,
      "metadata": {}
  }
  ```

### Golden Dataset Requirements
- **Axial-Flair Case:** Plane="Axial", Sequence="FLAIR", Depth="0.45", Narrative="Positive for hyperintense signal...", Confidence=0.99.
- **Sagittal T1 Case:** Plane="Sagittal", Sequence="T1", Depth="0.12", Narrative=None (Status: Skipped), Confidence=0.97.

### Implementation Guardrails
- **Mock-First Development:** This engine is critical for future UI/PDF stories (3.x and 4.x) before live models are ready.
- **Decoupling:** Ensure the mock logic doesn't require live model weights or GPU presence.

## References

- **PRD:** `docs/_bmad_output/planning-artifacts/prd.md#Success Criteria`
- **Architecture:** `docs/_bmad_output/planning-artifacts/architecture.md#Source Code Map`
- **UX Design:** `docs/_bmad_output/planning-artifacts/ux-design-specification.md#3.3 The Defensive Failover`
- **Previous Story 1.2:** `docs/_bmad_output/implementation-artifacts/1-2-centralized-state-management-inferencestate.md`

## Dev Agent Record

### Agent Model Used
Gemini 2.4 Pro

### Debug Log References
- Mock orchestration logic implemented in `src/logic/logic_gate.py`.
- UI updated to display metrics and narrative when inference is complete.
- Technical logs view enhanced with expanders for each step log.

### Completion Notes List
- Implemented `GOLDEN_DATASETS` with Axial-FLAIR and Sagittal-T1 scenarios.
- Created `run_mock_inference` to populate `st.session_state.inference`.
- Integrated scenario selection in Streamlit sidebar.
- Added unit tests for both utility and orchestration logic.

### File List
- `src/utils/mock_data.py`
- `src/logic/logic_gate.py`
- `app.py`
- `tests/test_mock_data.py`
- `tests/test_logic_gate.py`

### Change Log
- **2026-05-12**: Initial implementation of Mock Mode and Golden Datasets.
