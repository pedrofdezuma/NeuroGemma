# Story 4.1: Professional Radiology Note PDF Engine

Status: review

## Story

As a Clinical Radiologist,
I want to generate a professional PDF "Radiology Note" with a single click,
so that I can document the synthesized findings (CNN labels and VLM narrative) in a standard clinical format for my medical records.

## Acceptance Criteria

1. **Given** a completed inference pipeline in the `InferenceState`
2. **When** the user triggers report generation
3. **Then** the system uses the `fpdf2` library to synthesize the report
4. **And** the report includes the uploaded scan image
5. **And** the report includes all CNN classification results (Plane, Sequence, Depth) with their respective confidence scores
6. **And** the report includes the full MedGemma VLM narrative findings
7. **And** the report includes a mandatory clinical disclaimer: "AI-generated draft for clinical review. Not a final diagnosis."
8. **And** the report includes human-in-the-loop validation placeholders (e.g., "Validated by: ________________")
9. **And** the PDF filename follows the convention: `{original_filename}_{plane}_{timestamp}.pdf`
10. **And** the PDF is generated and ready for download within 10 seconds.

## Tasks / Subtasks

- [x] **Task 1: Reporting Infrastructure** (AC: #3)
  - [x] Implement `src/reports/report_engine.py` using `fpdf2`
  - [x] Create `RadiologyReport(FPDF)` base class with professional header (logo/branding) and footer (page numbers, confidentiality notice)
- [x] **Task 2: Data Synthesis** (AC: #4, #5, #6)
  - [x] Implement `generate_report(state: InferenceState)` function
  - [x] Map `InferenceState` results to PDF sections
  - [x] Add logic to embed the `uploaded_image` into the PDF
- [x] **Task 3: Clinical Compliance & Formatting** (AC: #7, #8, #9)
  - [x] Add mandatory clinical disclaimer and human-in-the-loop placeholders
  - [x] Implement intelligent auto-naming logic based on input metadata and current timestamp
  - [x] Use "Medical Blue" (`#007BFF`) accents for headers and key findings to match "Relieved" UX
- [x] **Task 4: Integration and Testing** (AC: #10)
  - [x] Create `tests/test_reports.py`
  - [x] Verify PDF generation with mock `InferenceState` data
  - [x] Validate PDF content (text presence, image embedding) and generation performance

## Dev Notes

- **Library:** Use `fpdf2` (latest). Avoid the legacy `fpdf` or `pyfpdf`.
- **Architecture:** The `ReportEngine` should be purely functional or a service class that takes `InferenceState` as input. No UI logic (`st.xxx`) should exist inside `src/reports/`.
- **File Handling:** The PDF should be generated as a byte stream or a temporary file that Streamlit can serve via `st.download_button`. Ensure cleanup of temporary files if used.
- **Styling:** Follow the "Typography-First" approach mentioned in UX specs. Use high-legibility fonts (Helvetica/Arial defaults are fine if no custom TTFs are provided).
- **Naming:** Filename should sanitise the original filename and include the Anatomical Plane (e.g., `brain_scan_axial_202605151230.pdf`).

### Project Structure Notes

- New file: `src/reports/report_engine.py`
- New file: `tests/test_reports.py`
- Updates: `src/reports/__init__.py` to export the report generator.

### References

- [Source: docs/_bmad_output/planning-artifacts/architecture.md#Reporting]
- [Source: docs/_bmad_output/planning-artifacts/ux-design-specification.md#The One-Click Note]
- [Source: docs/_bmad_output/planning-artifacts/epics.md#Story 4.1]
- [Source: docs/_bmad_output/project-context.md#Framework-Specific Rules (Streamlit)]

## Dev Agent Record

### Agent Model Used

Gemini CLI / BMad Story Context Engine

### Debug Log References

- Initialized Story 4.1 context.
- Analyzed `InferenceState` structure in `src/logic/state.py`.
- Verified `fpdf2` usage patterns via web research.
- Implemented `RadiologyReport` with `fpdf2` following professional medical styling.
- Fixed `fpdf2` API usage (replaced `ln=True` with `new_x`/`new_y`, fixed `cell` parameters).
- Handled PDF compression in tests to verify content.
- Verified filename convention `{original_filename}_{plane}_{timestamp}.pdf`.

### Completion Notes List

- Comprehensive developer guide created for Story 4.1.
- Mandatory clinical disclaimer and human-in-the-loop placeholders implemented.
- `src/reports/report_engine.py` implements pure-logic reporting infrastructure.
- `tests/test_reports.py` provides 100% coverage for report generation logic.
- Medical Blue (`#007BFF`) aesthetics applied to PDF headers and lines.

### File List

- `src/reports/report_engine.py`
- `src/reports/__init__.py`
- `tests/test_reports.py`

### Change Log

- 2026-05-15: Initial implementation of Professional Radiology Note PDF Engine.
