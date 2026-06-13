# Story 4.4: Automatic Session Reset on Report Download

Status: review

## Story

As a User,
I want my session data to be automatically wiped after I download my report,
so that I can ensure patient privacy and prevent state leakage between different scans.

## Acceptance Criteria

1. **Given** a successful report generation and download button display
2. **When** the "Generate Radiology Note" download button is clicked
3. **Then** the `InferenceState` must be automatically reset (equivalent to a "Clear Session" action)
4. **And** the application must trigger a script rerun to return the UI to its initial upload state
5. **And** the browser must still receive the PDF report download despite the state reset

## Tasks / Subtasks

- [x] **Task 1: Implement Download Callback** (AC: #2, #3)
  - [x] Add `on_click=reset_state` to the `st.download_button` in `app.py`.
- [x] **Task 2: UI Reset Verification** (AC: #4)
  - [x] Ensure the rerun correctly clears the file uploader and results display.
- [x] **Task 3: Privacy Compliance Check** (AC: #5, NFR5)
  - [x] Verify that no temporary image files or state remnants persist after the download.

## Dev Notes

- **Streamlit Behavior:** `st.download_button` triggers a script rerun by default. Adding an `on_click` callback ensures the state reset happens as part of that rerun sequence.
- **Privacy First:** This story fulfills the "Mandatory Privacy Reset" requirement from the project context.
- **State Reset:** Use the existing `reset_state()` function from `src.logic.state`.
- **Bug Fix:** Fixed `generate_report` in `src/reports/report_engine.py` to return `bytes` instead of `bytearray` to avoid "Invalid binary data format" errors in Streamlit.

### Project Structure Notes

- **Updates:** `app.py` (Modify `st.download_button` implementation)
- **Reference:** `src.logic.state` (Import `reset_state`)

### References

- [Source: docs/_bmad_output/planning-artifacts/epics.md#Story 4.4]
- [Source: docs/_bmad_output/planning-artifacts/prd.md#NFR5]
- [Source: docs/_bmad_output/project-context.md#Mandatory Privacy Reset]
- [Source: src/logic/state.py#reset_state]

## Dev Agent Record

### Agent Model Used

Gemini CLI / BMad Story Context Engine

### Context Analysis Summary

- **Current State:** The "Clear Session" button in the sidebar already handles manual resets. The download button currently just provides the file and triggers a rerun without explicit reset.
- **Requirement:** Automate the reset to ensure privacy without requiring a second click from the user.
- **Mechanism:** Streamlit callbacks on download buttons are executed before the full rerun, making them ideal for state cleanup.

### Learning from Previous Work

- Story 1.4 implemented the manual `Clear Session` logic.
- Story 4.1 & 4.2 established the PDF generation and FAB placement.
- Integration of `on_click` in `st.download_button` is the most idiomatic way to handle "Cleanup on Download" in Streamlit.

### Completion Notes List

- Added `on_click=reset_state` to the floating action button (FAB) download button in `app.py`.
- Fixed a type compatibility issue in `src/reports/report_engine.py` where `fpdf2` output was returned as `bytearray`, causing Streamlit errors.
- Verified that `reset_state()` correctly wipes the `InferenceState` including uploaded images and inference results.
- Verified syntax correctness of modified files.

### File List

- `app.py`
- `src/reports/report_engine.py`
