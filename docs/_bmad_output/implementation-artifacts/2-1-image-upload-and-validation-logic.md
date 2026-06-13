# Story 2.1: image-upload-and-validation-logic

Status: in-progress

## Story

As a User,
I want the system to validate my uploaded brain scan image,
so that I only process supported file types (JPG, PNG) and receive clear feedback on errors.

## Acceptance Criteria

1. **File Format Validation:** The system must accept only JPG, JPEG, and PNG formats.
2. **Robust Validation:** Validation must check the file content/header, not just the extension.
3. **State Management:** The validated image (as a PIL Image or bytes) must be stored in `st.session_state.inference.uploaded_image`.
4. **UI Feedback:** Clear, non-alarming error messages must be displayed if an invalid file is uploaded.
5. **Success Indicator:** A successful upload must update `InferenceState.current_stage` to `PipelineStage.ID` and log the "Upload Success" event.
6. **Architectural Compliance:** Validation logic must reside in `src/utils/file_handler.py` to keep `app.py` focused on UI.

## Tasks / Subtasks

- [x] **Implement File Handling Utility**
  - [x] Create `src/utils/file_handler.py`.
  - [x] Implement `validate_and_load_image(uploaded_file)` using Pillow.
  - [x] Handle exceptions (corrupted files, unsupported formats) and return descriptive errors.
- [x] **Update State Management**
  - [x] Update `InferenceState` in `src/logic/state.py` to include `uploaded_image` and `image_metadata`.
  - [x] Ensure `reset_state()` clears the image data.
- [x] **Refine app.py Upload UI**
  - [x] Implement the "Enhanced Image Upload Area" as per UX spec.
  - [x] Connect `st.file_uploader` to the `file_handler` validation.
  - [x] Display the uploaded image clearly once validated.
  - [x] Trigger the first stage of the Decision Journal log upon successful upload.
- [x] **Testing & Validation**
  - [x] Create `tests/test_file_handler.py`.
  - [x] Test with valid JPG/PNG, corrupted files, and invalid formats (e.g., TXT).
  - [x] Verify state updates in `st.session_state.inference`.

## Dev Notes

### Architecture & Standards
- **Modular Monolith:** Keep validation in `src/utils/`. `app.py` should only call the utility.
- **Strict Typing:** Ensure all functions in `file_handler.py` use type hints.
- **Medical Blue Aesthetic:** Follow the margins and palette established in `src/utils/styles.py` and the UX spec.

### Source Tree Components
- `src/utils/file_handler.py` (New)
- `src/logic/state.py` (Modify `InferenceState`)
- `src/utils/styles.py` (Modify CSS)
- `app.py` (Modify Upload area)
- `tests/test_file_handler.py` (New)
- `tests/test_state.py` (Modify tests)

### Testing Standards
- Use `pytest`.
- Mock `streamlit` if necessary, but focus on testing the `file_handler` logic independently.

## References

- **PRD:** `docs/_bmad_output/planning-artifacts/prd.md#Functional Requirements` (FR1, FR2)
- **Architecture:** `docs/_bmad_output/planning-artifacts/architecture.md#Implementation Patterns`
- **UX Design:** `docs/_bmad_output/planning-artifacts/ux-design-specification.md#Component Strategy` (1. Image Upload Area)
- **Project Context:** `docs/_bmad_output/project-context.md#Critical Implementation Rules`

## Dev Agent Record

### Agent Model Used
Gemini 2.0 Flash

### Debug Log References
- `src/utils/file_handler.py` implementation complete.
- `tests/test_file_handler.py` created and passed.
- `src/logic/state.py` updated with `uploaded_image` and `image_metadata`.
- `app.py` updated with enhanced upload UI and breadcrumbs.
- `src/utils/styles.py` updated with `upload-container` CSS.
- Regression tests in `tests/test_state.py` updated and passed.

### Completion Notes List
- Implemented robust image validation utility in `src/utils/file_handler.py`.
- Enhanced `InferenceState` to track uploaded images and metadata.
- Refined `app.py` with a "Medical Blue" themed upload area and pipeline breadcrumbs.
- Integrated event logging for successful uploads in the Decision Journal.
- All unit and integration tests (10/10) passed.

### File List
- `src/utils/file_handler.py`
- `src/logic/state.py`
- `src/utils/styles.py`
- `app.py`
- `tests/test_file_handler.py`
- `tests/test_state.py`

## Status
review
