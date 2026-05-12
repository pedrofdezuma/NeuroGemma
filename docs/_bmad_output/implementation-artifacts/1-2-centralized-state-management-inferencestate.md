# Story 1-2: Centralized State Management (InferenceState)

Status: review

## Story

As a Developer,
I want to implement a centralized `InferenceState` class in `st.session_state`,
So that I can track model results, pipeline progress, and technical logs across the application session.

## Acceptance Criteria

1. **Structured State Object:** A structured `InferenceState` object is created and maintained in `st.session_state.inference`.
2. **Pipeline Stages:** The state includes a `current_stage` field using an Enum (ID, GATE, SYNTHESIS, COMPLETE) to drive the UI Breadcrumbs.
3. **Model Results:** The state includes a `results` dictionary to store quantitative (CNN) and qualitative (VLM) outputs.
4. **Decision Journal:** The state includes a `step_logs` list of dictionaries for structured technical logging (timestamp, stage, event, model_id, outcome, confidence, metadata).
5. **Initialization Logic:** The state is automatically initialized on app startup if it doesn't exist, and can be reset via a dedicated function.

## Tasks / Subtasks

- [x] **Implement State Definitions** (AC: #2, #3, #4)
  - [x] Create `src/logic/state.py`
  - [x] Define `PipelineStage` Enum: `ID`, `GATE`, `SYNTHESIS`, `COMPLETE`
  - [x] Define `InferenceState` dataclass with type hints:
    - `current_stage`: `PipelineStage` (default: `ID`)
    - `results`: `dict[str, any]` (default: empty)
    - `step_logs`: `list[dict[str, any]]` (default: empty)
    - `is_mock_mode`: `bool` (default: `False`)
- [x] **Implement State Management Logic** (AC: #1, #5)
  - [x] Add `init_state()` function in `src/logic/state.py` to safely initialize `st.session_state.inference`
  - [x] Add `reset_state()` function to wipe the state (privacy requirement)
- [x] **Integrate with Entry Point** (AC: #1, #5)
  - [x] Update `app.py` to import and call `init_state()` at the very beginning of execution
- [x] **Validation & Testing**
  - [x] Create `tests/test_state.py` to verify the dataclass structure and default values
  - [x] Verify that `app.py` runs without errors and initializes the state object

## Dev Notes

### Architecture & Standards
- **Naming:** Use `PascalCase` for the `InferenceState` class and `PipelineStage` enum.
- **Location:** `src/logic/state.py` as per the "Modular Monolith" structure. [Source: `architecture.md`]
- **Strict Typing:** Mandatory use of type hints for the dataclass and all functions. [Source: `project-context.md`]
- **UI Decoupling:** `src/logic/state.py` should only define the data structure. While `init_state` will interact with `st.session_state`, keep the dataclass itself independent of Streamlit if possible (or accept the dependency for state management convenience).

### Technical Requirements
- **Structured Logs Format:** All entries in `step_logs` must follow this schema:
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
- **Privacy First:** The `reset_state` function is critical for the "Clear Session" requirement.

### Implementation Guardrails
- **No Session Bloat:** Do not store large objects (images, model weights) directly in `InferenceState`. Store them as file paths or use `@st.cache_resource`. [Source: `project-context.md`]

## References

- **PRD:** `docs/_bmad_output/planning-artifacts/prd.md#Additional Requirements`
- **Architecture:** `docs/_bmad_output/planning-artifacts/architecture.md#Data Architecture`
- **UX Design:** `docs/_bmad_output/planning-artifacts/ux-design-specification.md#2.5 Experience Mechanics`
- **Project Context:** `docs/_bmad_output/project-context.md#Framework-Specific Rules (Streamlit)`

## Dev Agent Record

### Agent Model Used
Gemini 2.0 Flash

### Debug Log References
- Tests run using Conda environment `neuro_env` located at `C:\Users\pedro\anaconda3\envs\neuro_env`.
- Pytest run with `PYTHONPATH="."`.

### Completion Notes List
- Implemented `PipelineStage` Enum and `InferenceState` dataclass in `src/logic/state.py`.
- Added `init_state` and `reset_state` functions for session management.
- Integrated state initialization in `app.py`.
- Connected "Mock Mode" and "Clear Session" UI elements in `app.py` to the centralized state.
- Created comprehensive unit tests in `tests/test_state.py` covering all ACs and technical requirements.

### File List
- src/logic/state.py (NEW)
- app.py (UPDATE)
- tests/test_state.py (NEW)

### Change Log
- 2026-05-12: Implemented centralized state management. Added InferenceState dataclass and integrated with app.py. Passed all unit tests.
