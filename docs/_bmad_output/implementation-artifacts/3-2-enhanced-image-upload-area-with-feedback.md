# Story 3.2: Enhanced Image Upload Area with Feedback

Status: review

## Story

As a User,
I want an intuitive drag-and-drop area for uploading my brain scans,
so that I can easily initiate the inference process with clear visual feedback and professional clinical confidence.

## Acceptance Criteria

1. **Given** the "Diagnostic View" tab
2. **When** I view the upload area
3. **Then** it displays a clear drag-and-drop target with instruction text: "Drag & Drop Brain Scan Here or Click to Upload".
4. **And** it provides visual feedback for **Hover** state (CSS transition of border and background color).
5. **And** it provides visual feedback for **Loading** state (using `st.spinner` or `st.status` during image validation and state initialization).
6. **And** it provides visual feedback for **Success** state (displaying a brief confirmation message or showing the image before transitioning to the split-screen dashboard).
7. **And** it provides clear error feedback (using `st.error`) if an unsupported file type or corrupted image is uploaded.
8. **And** the entire area follows the "Relieved" aesthetic (2rem margins, Medical Blue `#007BFF` accents, and minimalist typography).

## Tasks / Subtasks

- [x] **Enhance Upload Styling in `styles.py`** (AC: #4, #8)
  - [x] Add `.upload-icon` CSS for a clinical upload icon (using an emoji or SVG).
  - [x] Refine `.upload-container` to ensure it encapsulates the `st.file_uploader` widget cleanly.
  - [x] Add a `success-pulse` or similar animation/class for the success state if needed.
- [x] **Refactor Upload Logic in `app.py`** (AC: #3, #5, #6, #7)
  - [x] Wrap `st.file_uploader` in a more robust container with the clinical icon and instruction text.
  - [x] Implement `st.status("🩺 Validating Scan...", expanded=False)` during the `validate_and_load_image` call.
  - [x] Add a brief `st.toast("✅ Image Validated Successfully")` or `st.success` before the `st.rerun()`.
  - [x] Ensure `label_visibility="collapsed"` is maintained for the native uploader to keep the "Relieved" focus.
- [x] **Improve "Zero State" Experience** (AC: #3)
  - [x] Ensure the upload area is centered and provides enough whitespace (using the `2rem` margin guardrail).
  - [x] Add a subtle secondary instruction about supported formats (JPG/PNG).

## Dev Notes

- **Reuse Existing Logic:** Do NOT reinvent the validation logic. Use `src/utils/file_handler.validate_and_load_image`.
- **Relieved Aesthetic:** Maintain the `2rem` margins. The upload area should feel "airy" and professional, not cramped.
- **State Management:** Ensure `st.session_state.inference` is updated correctly with `uploaded_image` and `image_metadata` before rerunning.
- **Mock Mode Consistency:** Ensure that when Mock Mode is ON, the upload area still works as the entry point for custom images, or clearly indicates that Mock Data can be loaded via the sidebar.

### Project Structure Notes

- **`src/utils/styles.py`**: Centralized location for all CSS enhancements.
- **`app.py`**: Location for the UI orchestration logic in `tab_diag`.
- **`src/utils/file_handler.py`**: Existing validation logic to be called.

### References

- **UX Spec:** [docs/_bmad_output/planning-artifacts/ux-design-specification.md#Component Strategy] (Component 1: Image Upload Area)
- **Architecture:** [docs/_bmad_output/planning-artifacts/architecture.md#Frontend Architecture]
- **Previous Story (3.1):** [docs/_bmad_output/implementation-artifacts/3-1-relieved-aesthetic-and-two-tab-layout.md] (Established the base 'Relieved' styles)

## Dev Agent Record

### Agent Model Used
Gemini 2.0 Flash

### Completion Notes List
- Analysis of PRD, Architecture, and UX specs completed.
- Existing `app.py` and `styles.py` analyzed for enhancement points.
- Acceptance criteria for feedback states (Hover, Loading, Success) formalized.
- Transition strategy from upload to dashboard defined.
- **Implementation (2026-05-15):**
  - Enhanced `styles.py` with `.upload-icon`, `.upload-subtext`, and `.success-pulse` classes.
  - Refactored `app.py` to use a custom HTML container for the upload area with a clinical emoji icon.
  - Integrated `st.status` for real-time validation feedback.
  - Added `st.toast` and `st.success` for successful upload confirmation.
  - Added clinical subtext for supported file formats.
  - Verified with updated unit tests in `tests/test_styles.py` and full regression suite.

### File List
- `app.py`
- `src/utils/styles.py`
- `tests/test_styles.py`
- `src/utils/file_handler.py` (Reference only)

## Change Log

- **2026-05-15:** Initial implementation of enhanced upload area and logic refactoring. Addressing all ACs.
