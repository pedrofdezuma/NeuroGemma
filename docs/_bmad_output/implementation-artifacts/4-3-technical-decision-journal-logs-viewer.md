# Story 4.3: Technical "Decision Journal" (Logs Viewer)

Status: review

## Story

As a Thesis Evaluator,
I want to see a structured "Decision Journal" of the AI's orchestration logic,
so that I can verify the engineering integrity and Logic Gate decisions during the clinical demonstration.

## Acceptance Criteria

1. **Given** the "Technical Logs" tab in the application
2. **When** the inference pipeline is running or complete
3. **Then** the "Decision Journal" displays a structured, human-readable audit trail of all pipeline events
4. **And** each log entry includes a formatted timestamp (HH:MM:SS), the pipeline stage (ID, GATE, SYNTHESIS), the specific event, and the outcome
5. **And** model classifications (Plane, Sequence, Depth) prominently display their numerical confidence scores (e.g., 99.2%)
6. **And** the "Logic Gate" decision is clearly highlighted to show if the VLM was triggered or bypassed
7. **And** raw technical metadata (e.g., CNN raw scores, VLM text length) is accessible but non-intrusive (e.g., inside a sub-expander or code block)
8. **And** the UI maintains the "Relieved" aesthetic with clean spacing and professional typography

## Tasks / Subtasks

- [x] **Task 1: Define Journal Styling** (AC: #8)
  - [x] Add CSS to `src/utils/styles.py` for the Decision Journal entries (e.g., `.journal-entry`, `.journal-timestamp`, `.journal-badge`).
  - [x] Ensure the log colors align with the existing status colors (Blue for ID, Gray for Skip, Green for Success).
- [x] **Task 2: Implement Structured Log Display** (AC: #3, #4, #5, #6)
  - [x] Update `app.py` in the `tab_logs` section to replace the basic `st.json` loop with a structured layout.
  - [x] Use `st.columns` or a custom HTML table to show: Time | Stage | Event | Outcome | Confidence.
  - [x] Format confidence scores as percentages with one decimal place.
- [x] **Task 3: Metadata Accessibility** (AC: #7)
  - [x] Implement an "inspector" view for each log entry (e.g., an expander inside the journal row) to show the `metadata` dictionary.
- [x] **Task 4: Zero-State and Real-Time Updates** (AC: #3)
  - [x] Ensure the journal updates in real-time as the pipeline executes (since `run_pipeline` is a generator).
  - [x] Maintain a professional "Empty State" message when no logs are present.

## Dev Notes

- **Data Source:** Use `st.session_state.inference.step_logs`, which is a list of dictionaries.
- **Timestamp Formatting:** Convert the ISO-8601 strings in the logs to a user-friendly `HH:MM:SS` format.
- **Status Mapping:** Map `GATE_DECISION` outcomes ("TRIGGERED"/"SKIPPED") to distinct visual styles to make the Logic Gate behavior obvious.
- **Confidence Logic:** Not all logs have a `confidence` field. Handle missing values gracefully.
- **UI Decoupling:** Keep the presentation logic in `app.py` (or a helper in `src/utils/styles.py`) and do not modify the core logging logic in `src/logic/logic_gate.py` unless absolutely necessary.

### Project Structure Notes

- **Updates:** `src/utils/styles.py` (New Journal CSS)
- **Updates:** `app.py` (Tab Logs UI implementation)
- **Reference:** `src/logic/state.py` (Log schema)
- **Reference:** `src/logic/logic_gate.py` (Log generation points)

### References

- [Source: docs/_bmad_output/planning-artifacts/ux-design-specification.md#6. Technical Logs Viewer (Structured Decision Journal)]
- [Source: docs/_bmad_output/planning-artifacts/epics.md#Story 4.3]
- [Source: src/logic/state.py]
- [Source: src/logic/logic_gate.py]

## Dev Agent Record

### Agent Model Used

Gemini CLI / BMad Story Context Engine

### Context Analysis Summary

- **State:** `InferenceState` already contains `step_logs` with a structured dictionary format.
- **Logic:** `logic_gate.py` already appends logs at critical path points (Upload, CNNs, Gate, VLM).
- **Current UI:** `app.py` has a placeholder loop using `st.json` which is too technical and cluttered for a "clinical" demo.
- **Requirement:** Transition to a "Decision Journal" that is "human-readable" and "structured".

### Learning from Previous Work

- Story 4.2 successfully implemented the FAB using `fixed` positioning in CSS.
- The `PipelineStage` enum is reliably used for breadcrumbs; it should also drive the journal stage badges.
- `st.status` and generators in `logic_gate.py` ensure the UI stays reactive.

### Completion Notes List

- Implemented structured "Decision Journal" in the Technical Logs tab.
- Added custom CSS for journal rows, badges, and outcome highlights in `src/utils/styles.py`.
- Formatted confidence scores as prominent percentages (e.g., 99.2%) in the journal view.
- Added an "Inspector" expander for each log entry to allow access to raw technical metadata without cluttering the UI.
- Implemented a clean "Empty State" for the logs viewer.
- Verified that logs are chronological and capture all major pipeline events (Upload, CNNs, Gate, VLM).

## File List

- `src/utils/styles.py`
- `app.py`

## Change Log

- 2026-05-15: Initial implementation of Decision Journal styles and UI.
