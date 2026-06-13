# Story 3.4: Unified Diagnostic Results Display

Status: review

## Story

As a User,
I want to see all model outputs (labels, tags, and narrative) in a single horizontal layout,
So that I can synthesize the diagnostic findings effortlessly and trust the AI's orchestration decisions.

## Acceptance Criteria

1. **Given** completed inference results
2. **When** I view the "Diagnostic View"
3. **Then** the CNN labels (Plane, Sequence, Depth) are displayed as color-coded cards with confidence scores.
4. **And** the MedGemma VLM narrative is displayed as clear, explainable text within a dedicated container.
5. **And** if the VLM was triggered, a success-colored "VLM Triggered" indicator (icon + text) is shown.
6. **And** if the VLM was skipped, a clear "VLM Skipped" indicator with the reason is shown.
7. **And** the layout follows the "Relieved" aesthetic (airy spacing, minimalist typography).

## Tasks / Subtasks

- [x] **Backend: Update results to include individual confidence scores** (AC: 3)
  - [x] Modify `src/logic/logic_gate.py` to store `plane_conf`, `sequence_conf`, and `depth_conf`.
  - [x] Update `src/utils/mock_data.py` to include these scores in Golden Datasets.
- [x] **Styling: Add CSS for color-coded cards and VLM status indicators** (AC: 3, 5, 6, 7)
  - [x] Define `.result-card` specialized classes (`.plane`, `.sequence`, `.depth`).
  - [x] Define `.confidence-tag` states (`.high`, `.med`, `.low`).
  - [x] Define `.vlm-status` and `.vlm-status.skipped` classes.
- [x] **UI: Implement the unified results display in `app.py`** (AC: 3, 4, 5, 6, 7)
  - [x] Refactor the Results column to use a loop for CNN cards with confidence tags.
  - [x] Implement conditional rendering for the VLM narrative and status indicator.
- [x] **Verification & Testing**
  - [x] Update `tests/test_logic_gate.py` to handle generator execution and verify new confidence fields.
  - [x] Verify UI in Mock Mode for both "Positive" and "Skipped" scenarios.

## Dev Notes

- **Modular Monolith:** UI logic resides in `app.py`, while orchestration is in `src/logic/logic_gate.py`.
- **State Management:** `st.session_state.inference` is the single source of truth for results.
- **Generator Pattern:** All pipeline execution functions return generators to support real-time UI updates (from Story 3.3).

### Project Structure Notes

- Alignment with unified project structure (paths, modules, naming)

### References

- [Source: docs/_bmad_output/planning-artifacts/ux-design-specification.md#Component 4: Logic Gate Trigger Indicator]
- [Source: docs/_bmad_output/planning-artifacts/architecture.md#Format Patterns]

## Dev Agent Record

### Agent Model Used

Gemini 1.5 Pro (via BMad Context Engine)

### Debug Log References

### Change Log
- Implemented individual confidence scores for Plane, Sequence, and Depth models.
- Added specialized CSS for color-coded result cards and VLM status indicators.
- Refactored UI to display unified diagnostic results with confidence tags.
- Updated mock data and tests to support new confidence fields.

### File List
- `app.py`
- `src/utils/styles.py`
- `src/logic/logic_gate.py`
- `src/utils/mock_data.py`
- `tests/test_logic_gate.py`
- `tests/test_story_3_4_confidence.py`
