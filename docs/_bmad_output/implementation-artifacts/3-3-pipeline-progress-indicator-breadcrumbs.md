# Story 3.3: Pipeline Progress Indicator (Breadcrumbs)

Status: review

## Story

As a User,
I want to see sequential "Pipeline Breadcrumbs" during inference,
So that I understand the system's progress during the 60-second latency period and feel confident in the AI's orchestration steps.

## Acceptance Criteria

1. **Given** an active inference pipeline (after clicking "Run Pipeline")
2. **When** a stage (ID, GATE, SYNTHESIS, COMPLETE) is executing
3. **Then** the corresponding breadcrumb in the UI lights up with an **Active** highlight (Clinical Blue `#007BFF`).
4. **And** completed stages are highlighted with a **Done** state (Success Green `#28A745`).
5. **And** the status updates in **real-time** without requiring a full page rerun between every stage transition.
6. **And** the breadcrumbs are positioned at the top of the Diagnostic View, following the "Relieved" aesthetic (airy spacing, minimalist typography).
7. **And** the implementation must respect the architectural boundary between `app.py` (UI) and `src/logic` (Inference logic).

## Tasks / Subtasks

- [x] **Refactor `src/logic/logic_gate.py` for Step-wise Execution**
  - [x] Convert `run_pipeline(image)` into a generator that `yield`s the `PipelineStage` at each transition.
  - [x] Ensure `inference.current_stage` is updated BEFORE each `yield`.
  - [x] Maintain the existing logic for CNNs, Logic Gate evaluation, and VLM triggering.
- [x] **Implement Real-time Breadcrumb Updates in `app.py`**
  - [x] Create a `render_breadcrumbs(stage)` helper function that returns the HTML string based on the current `InferenceState`.
  - [x] Replace the static breadcrumb rendering at the top of `app.py` with an `st.empty()` placeholder.
  - [x] Update the placeholder immediately upon page load with the current state.
  - [x] In the "Run Pipeline" button logic, iterate over the `run_pipeline` generator and update the `st.empty()` placeholder at each step.
- [x] **Refine Breadcrumb Styling in `src/utils/styles.py`**
  - [x] Verify `.breadcrumb-container` and `.breadcrumb-step` (active/done) classes meet the UX spec (low-saturation for active, green for done).
  - [x] Ensure the font size and spacing provide "Relieved" clinical focus.
- [x] **Verification & Testing**
  - [x] Verify the breadcrumbs update in real-time during a "Mock Mode" run (if applicable) and Live Mode.
  - [x] Ensure the "COMPLETE" stage persists after the pipeline finishes.
  - [x] Run existing integration tests to ensure no regressions in orchestration logic.

## Developer Context

### System Architecture
- **State Management:** `st.session_state.inference` (an `InferenceState` instance) is the source of truth for `current_stage`.
- **UI/Logic Split:** `app.py` handles the `st.*` calls and HTML rendering. `src/logic/logic_gate.py` handles the orchestration.
- **Generator Pattern:** Using a generator is the idiomatic Streamlit way to push updates to the UI from a long-running process without `st.rerun()`.

### Files to Modify
- **`src/logic/logic_gate.py`**: Refactor `run_pipeline` to yield stages.
- **`app.py`**: Implement the `st.empty()` placeholder and iteration logic.
- **`src/utils/styles.py`**: (If needed) Minor tweaks to breadcrumb CSS.

### Guardrails
- **NO RERUNS during pipeline:** Do NOT use `st.rerun()` inside the pipeline loop; it will reset the execution. Only use `st.rerun()` at the very end to finalize the full UI state if necessary.
- **Strict Typing:** Ensure all new function signatures use type hints (e.g., `def run_pipeline(image: Image.Image) -> Generator[PipelineStage, None, None]:`).
- **Logic Gate Integrity:** Do not change the underlying logic of when the VLM is triggered (Axial + FLAIR).

## Previous Story Intelligence (3.2)
- The "Success" state of the upload area now transitions to the split-screen dashboard.
- The "Run Pipeline" button is now the primary entry point for this story.
- Ensure the breadcrumbs are visible even before the pipeline starts (in the "ID" state).

## Git Intelligence
- Recent commits (53600f2, 786731a) established the `InferenceState` and basic logic gate.
- The project structure is stable; stick to the `src/` modular monolith pattern.

## Technical References
- **UX Spec:** [docs/_bmad_output/planning-artifacts/ux-design-specification.md#Component 2: Pipeline Progress Indicator]
- **Architecture:** [docs/_bmad_output/planning-artifacts/architecture.md#Frontend Architecture]
- **State Definition:** `src/logic/state.py`

## Completion Status
- [x] Logic refactored to Generator
- [x] Breadcrumb placeholder implemented in UI
- [x] Real-time update loop verified
- [x] Styling matches 'Relieved' aesthetic

## File List
- `src/logic/logic_gate.py`
- `app.py`
- `src/utils/styles.py`
- `tests/test_pipeline_generator.py` (New)
- `tests/test_styles.py` (Modified)
- `tests/test_pipeline_integration.py` (Modified)

## Change Log
- Refactored `run_pipeline` and `run_mock_inference` to generators in `src/logic/logic_gate.py`.
- Implemented `render_breadcrumbs` helper and `st.empty()` placeholder in `app.py` for real-time updates.
- Centralized breadcrumb HTML rendering in `src/utils/styles.py`.
- Added `test_pipeline_generator.py` and updated existing tests to verify generator behavior.
- Updated `sprint-status.yaml` to mark story as `review`.
