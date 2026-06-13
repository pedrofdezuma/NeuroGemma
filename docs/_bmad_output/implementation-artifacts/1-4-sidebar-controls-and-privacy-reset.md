# Story 1.4: Sidebar Controls and Privacy Reset

Status: review

## Story

As a User,
I want a sidebar with a Mock Mode toggle and a "Clear Session" button,
So that I can control the demo stability and ensure my clinical data is wiped after each run.

## Acceptance Criteria

1. [x] **Sidebar Organization:** The Streamlit sidebar includes a distinct section for "System Controls."
2. [x] **Mock Mode Toggle:**
    - A toggle switch to enable/disable "Mock Mode".
    - State is persisted in `InferenceState.is_mock_mode`.
    - UI immediately updates to show/hide "Golden Dataset" selection based on toggle state.
3. [x] **Privacy Reset (Clear Session):**
    - A "Clear Session" button is prominent in the sidebar.
    - Clicking the button calls `reset_state()` to wipe all results, logs, and image references.
    - The UI immediately reverts to the initial "Ready to Upload" state.
4. [x] **"Medical Blue" Aesthetic:**
    - Sidebar styling follows the UX specification (Medical Blue accents, clean spacing).
    - Custom CSS is loaded from `src/utils/styles.py`.
5. [x] **Architectural Compliance:**
    - `st.set_page_config` is the absolute first Streamlit command called in `app.py`.
    - No business logic or state resets are hardcoded in `app.py`; they use `src/logic/state.py`.

## Tasks / Subtasks

- [x] **Establish Styling Utility**
  - [x] Create `src/utils/styles.py` with `load_custom_css()` function.
  - [x] Implement the "Medical Blue" palette (`#007BFF`, `#2C3E50`, `#F8F9FA`) in CSS.
  - [x] Define styles for the Sidebar and the "Clear Session" button.
- [x] **Refine app.py Entry Point**
  - [x] Move `st.set_page_config` to be the first command in `main()`.
  - [x] Call `styles.load_custom_css()` at startup.
  - [x] Ensure the "Clear Session" button uses `reset_state()` and triggers a clean UI reset.
- [x] **Enhance Sidebar Controls**
  - [x] Group Mock Mode and Clear Session under a "Control Center" subheader.
  - [x] Add tooltips/help text to controls explaining their clinical/technical purpose.
- [x] **Validation & Privacy Verification**
  - [x] Verify that `reset_state()` completely clears `st.session_state.inference`.
  - [x] Confirm no image data or results persist after clicking "Clear Session".

## Dev Notes

### Architecture & Standards
- **Styling Strategy:** Use `src/utils/styles.py` to keep `app.py` clean. Inject CSS via `st.markdown(css, unsafe_allow_html=True)`.
- **Privacy First:** The "Clear Session" button is a mandatory requirement for clinical data handling standards. [Source: `epics.md#Additional Requirements`]
- **InferenceState:** Always use the `reset_state()` helper from `src/logic/state.py` to ensure consistency.

### UX Specifics
- **Primary Color:** `#007BFF` (Clinical Blue).
- **Reset Button:** Should be clear and perhaps use a secondary style to avoid accidental clicks while still being accessible.
- **Whitespace:** Ensure generous margins as per the "Relieved" aesthetic.

## References

- **PRD:** `docs/_bmad_output/planning-artifacts/prd.md#Functional Requirements` (FR18, FR10)
- **Architecture:** `docs/_bmad_output/planning-artifacts/architecture.md#Frontend Architecture`
- **UX Design:** `docs/_bmad_output/planning-artifacts/ux-design-specification.md#2.5 Experience Mechanics`
- **Previous Story 1.3:** `docs/_bmad_output/implementation-artifacts/1-3-mock-mode-engine-and-golden-datasets.md`

## Dev Agent Record

### Agent Model Used
Gemini 2.0 Flash

### Debug Log References
- Environment verification using full Conda path.
- Red-Green-Refactor for `src/utils/styles.py`.
- Validation of `reset_state()` via unit tests.

### Completion Notes List
- Implemented `src/utils/styles.py` for centralized CSS management.
- Reorganized `app.py` to satisfy `st.set_page_config` precedence requirements.
- Enhanced sidebar with tooltips and clinical branding.
- Verified privacy reset functionality via `tests/test_state.py`.

### File List
- `src/utils/styles.py` (New)
- `tests/test_styles.py` (New)
- `app.py` (Modified)
- `tests/test_state.py` (Verified existing/Modified for clarity)

### Change Log
- **2026-05-13**: Initial story creation by Ultimate Context Engine.
- **2026-05-13**: Implementation complete. Added CSS utility and sidebar refinements.
