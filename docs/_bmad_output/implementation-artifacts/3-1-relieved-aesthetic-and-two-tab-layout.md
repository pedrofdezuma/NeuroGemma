# Story 3.1: Relieved Aesthetic and Two-Tab Layout

Status: review

## Story

As a User,
I want a minimalist "Medical Blue" interface with a Two-Tab layout,
So that I can focus on my diagnosis in a calm environment while still having access to technical logs.

## Acceptance Criteria

1. **Given** the `app.py` entry point
2. **When** I load the application
3. **Then** the "Medical Blue" color palette and "Relieved" spacing (2rem margins) are applied via custom CSS.
4. **And** the UI is divided into two tabs: "Diagnostic View" (primary) and "Technical Logs" (secondary).
5. **And** the "Diagnostic View" utilizes a Wide/Fluid split-screen layout (Left: Image Viewer, Right: Results/Narrative).
6. **And** the interface is optimized for a 1080p desktop workstation, following the "Relieved" UX philosophy.
7. **And** custom CSS is centralized in `src/utils/styles.py` as per architectural guardrails.

## Tasks / Subtasks

- [x] **Establish "Medical Blue" Theme & Typography** (AC: #3)
  - [x] Update `.streamlit/config.toml` with primary colors and sans-serif font.
  - [x] Implement `Inter` or `Open Sans` font import in `src/utils/styles.py`.
- [x] **Implement "Relieved" CSS Framework** (AC: #3, #6)
  - [x] Define `block-container` padding (2rem) in `src/utils/styles.py`.
  - [x] Create `.result-card` and `.narrative-container` CSS classes.
  - [x] Define breadcrumb and FAB positioning styles.
- [x] **Refactor `app.py` for Two-Tab Layout** (AC: #4)
  - [x] Implement `st.tabs(["📋 Diagnostic View", "⚙️ Technical Logs"])`.
  - [x] Ensure `init_state()` and `load_custom_css()` are called at the very beginning of `main()`.
  - [x] Preserve existing Sidebar controls (Mock Mode toggle, Clear Session) but ensure they are visually consistent with the new theme.
- [x] **Design Wide/Fluid Diagnostic Dashboard** (AC: #5)
  - [x] Implement `st.columns([1.2, 1])` for image vs. results split.
  - [x] Place `st.image` in the left column with a high-contrast (black) container using the `.result-card` class with inline black background.
  - [x] Place quantitative results (CNN cards) and qualitative narrative (VLM text) in the right column.
- [x] **UI Component Refinement** (AC: #3, #6)
  - [x] Update existing Breadcrumbs logic in `app.py` to use the `.breadcrumb-container` and `.breadcrumb-step` CSS classes instead of hardcoded styles.
  - [x] Enhance "Image Upload Area" with dashed borders and hover effects using the `.upload-container` class.
  - [x] Implement placeholder "Generate Radiology Note" FAB at bottom-right using the `.fab-container` class.
  - [x] Ensure all components use the new CSS classes for visual consistency.

## Dev Notes

- **Relieved Aesthetic:** Prioritize whitespace and calm colors. Avoid clutter. Margins should be a consistent 2rem.
- **Architecture Compliance:**
  - `app.py` must only contain UI logic. No business logic or model inference rules.
  - `src/utils/styles.py` is the single source of truth for custom CSS. Do NOT create new CSS files.
  - Use `InferenceState` from `src/logic/state.py` to drive all UI changes.
- **Existing Functionality:** Do not break the Mock Mode or the `run_pipeline` integration established in Epic 2.
- **Testing:** Verify layout responsiveness on 1080p. Check that CSS classes are correctly applied to HTML elements generated via `st.markdown`.

### Project Structure Notes

- `src/utils/styles.py`: Centralized CSS.
- `app.py`: UI Orchestration.
- `.streamlit/config.toml`: Global theme settings.

### References

- **PRD:** [docs/_bmad_output/planning-artifacts/prd.md#Functional Requirements] (FR10, FR11, FR22)
- **UX Spec:** [docs/_bmad_output/planning-artifacts/ux-design-specification.md#Visual Design Foundation]
- **Architecture:** [docs/_bmad_output/planning-artifacts/architecture.md#Frontend Architecture]

## File List

- `src/utils/styles.py` (Verified/Formalized)
- `app.py` (Verified/Formalized)
- `.streamlit/config.toml` (Verified/Formalized)
- `tests/test_styles.py` (Modified - added comprehensive tests)

## Change Log

- 2026-05-15: Verified implementation of 'Relieved' aesthetic and two-tab layout.
- 2026-05-15: Added comprehensive CSS class tests in `tests/test_styles.py`.

## Dev Agent Record

### Agent Model Used
Gemini 2.0 Flash

### Completion Notes List
- Analysis of PRD, Architecture, and UX specs completed.
- CSS classes for "Relieved" aesthetic defined.
- Split-screen layout strategy formulated.
- Story document generated and ready for implementation.
- VERIFIED: All "Relieved" aesthetic requirements (2rem margins, Medical Blue, split-screen) are correctly implemented in `app.py` and `styles.py`.
- ADDED: Unit tests for all custom CSS classes to ensure visual consistency guardrails.
- VALIDATED: Full regression suite passing.
