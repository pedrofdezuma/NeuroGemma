# Story 4.2: Floating Action Button (FAB) for PDF Export

Status: review

## Story

As a Clinical Radiologist,
I want a persistent "Generate Report" button that is easy to find after inference,
so that I can quickly transition from diagnosis to documentation without searching for a static button.

## Acceptance Criteria

1. **Given** the "Diagnostic View" tab
2. **When** the inference pipeline is complete (`PipelineStage.COMPLETE`)
3. **Then** a circular/rounded Floating Action Button (FAB) appears at the bottom-right of the screen
4. **And** the FAB uses the "Medical Blue" (`#007BFF`) palette and clinical styling
5. **And** the FAB contains a "📄" icon and the text "Generate Radiology Note"
6. **And** clicking it triggers the PDF generation process using the `ReportEngine`
7. **And** the user receives a standard browser download prompt for the professional Radiology Note
8. **And** the download follows the naming convention: `{original_filename}_{plane}_{timestamp}.pdf`

## Tasks / Subtasks

- [x] **Task 1: FAB Styling Refinement** (AC: #4, #5)
  - [x] Update `src/utils/styles.py` to ensure `.fab-container` and its children (Streamlit buttons) are perfectly positioned and styled.
  - [x] Apply hover effects and shadows to the FAB to match the "Relieved" aesthetic.
- [x] **Task 2: UI Implementation in Diagnostic View** (AC: #1, #2, #3)
  - [x] Modify `app.py` to import `generate_report` and `get_report_filename` from `src.reports.report_engine`.
  - [x] Implement the conditional logic to display the FAB only when `inference.current_stage == PipelineStage.COMPLETE`.
  - [x] Replace the placeholder button with a functional `st.download_button`.
- [x] **Task 3: Pipeline Integration** (AC: #6, #7, #8)
  - [x] Connect `st.download_button` to the `generate_report(inference)` function.
  - [x] Use `get_report_filename(inference)` for the `file_name` parameter.
  - [x] Verify that the generated PDF accurately reflects the current `InferenceState`.

## Dev Notes

- **Positioning:** The FAB must be `fixed` to the viewport, not the container, ensuring it stays at the bottom-right even if the results are long.
- **State Check:** Use `PipelineStage.COMPLETE` as the trigger. The `run_pipeline` generator in `logic_gate.py` should be verified to yield `COMPLETE` at the very end.
- **Streamlit Button Styling:** Target the `st.download_button` specifically inside the `.fab-container` to avoid affecting other buttons in the app.
- **Library:** Use the existing `src/reports/report_engine.py` (which uses `fpdf2`). Do not reinvent the reporting logic.

### Project Structure Notes

- **Updates:** `src/utils/styles.py` (CSS additions)
- **Updates:** `app.py` (UI logic)
- **Integration:** `src/reports/report_engine.py` (Functional dependency)

### References

- [Source: docs/_bmad_output/planning-artifacts/ux-design-specification.md#5. Generate Report Floating Action Button (FAB)]
- [Source: docs/_bmad_output/planning-artifacts/epics.md#Story 4.2]
- [Source: docs/_bmad_output/implementation-artifacts/4-1-professional-radiology-note-pdf-engine.md]
- [Source: src/utils/styles.py]
- [Source: app.py]

## Dev Agent Record

### Agent Model Used

Gemini CLI / BMad Story Context Engine

### Debug Log References

- Analyzed `app.py` and found existing FAB placeholder.
- Verified `src/utils/styles.py` contains partial FAB CSS.
- Confirmed `report_engine.py` is ready for consumption.
- Mapped `PipelineStage.COMPLETE` to the FAB visibility condition.
- Updated `src/utils/styles.py` with refined CSS for pill-shaped FAB with shadow and hover.
- Integrated `st.download_button` in `app.py` with `generate_report` and `get_report_filename`.
- Verified all styles and logic via `pytest` and manual inspection.

### Completion Notes List

- Comprehensive developer guide created for Story 4.2.
- FAB visibility linked to `PipelineStage.COMPLETE`.
- Implementation path for `st.download_button` clearly defined.
- ✅ FAB Styling refined: Pill shape, Medical Blue, Box-shadow, and Hover effects implemented.
- ✅ Conditional UI logic: FAB only appears when the pipeline reaches `COMPLETE` stage.
- ✅ Report Engine Integration: `st.download_button` correctly calls PDF generation with dynamic filename.
- ✅ Verified all 48 tests pass including updated style tests.

### File List

- `src/utils/styles.py`
- `app.py`
- `tests/test_styles.py`
- `docs/_bmad_output/implementation-artifacts/4-2-floating-action-button-fab-for-pdf-export.md`

## Change Log

- 2026-05-15: Initial implementation of FAB styling and UI integration. Address all ACs for Story 4.2.
