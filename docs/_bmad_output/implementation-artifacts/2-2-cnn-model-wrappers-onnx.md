# Story 2-2: CNN Model Wrappers (ONNX)

## Story Header
**ID:** 2-2
**Key:** 2-2-cnn-model-wrappers-onnx
**Status:** review
**Epic:** 2 - Intelligent Inference Engine (The Logic Gate)
**Priority:** High
**Estimated Effort:** Medium

## Story Requirements
**User Story Statement:**
As a Developer,  
I want to implement independent wrappers for the three CNN models (Plane, Sequence, Depth) using ONNX Runtime,  
So that I can perform high-speed quantitative classification on local hardware.

**Acceptance Criteria (BDD):**
*   **Given** an input image (PIL object or numpy array)
*   **When** the CNN inference is triggered via the wrapper classes
*   **Then** the system classifies Anatomical Plane (Axial/Sagittal/Coronal), Sequence (T1/T2/FLAIR), and Depth
*   **And** each result includes a numerical confidence score (0.0 to 1.0)
*   **And** the wrappers handle their own preprocessing (resizing to model input size, normalization)
*   **And** the entire CNN stage (all 3 models) completes within 30 seconds.

## Developer Context
This story implements the first stage of the Intelligent Inference Engine. These CNN wrappers will be called by the `LogicGate` in a subsequent story.

### Technical Requirements
*   **Framework:** `onnxruntime` (for CPU/GPU inference).
*   **Imaging:** `pillow` (PIL) for image manipulation.
*   **Numerical:** `numpy` for tensor formatting and post-processing (softmax).
*   **Type Safety:** Use explicit type hints (e.g., `dict[str, Any]`, `np.ndarray`, `Image.Image`).
*   **Caching:** Use `@st.cache_resource` for loading `InferenceSession` to avoid reloading weights on every run.

### Architecture Compliance
*   **File Location:** Place model wrappers in `src/models/`.
*   **Naming Conventions:**
    *   Files: `model_plane_cnn.py`, `model_seq_cnn.py`, `model_depth_cnn.py`.
    *   Classes: `ModelPlaneCNN`, `ModelSeqCNN`, `ModelDepthCNN`.
*   **Pattern:** Each class should have a `predict(self, image: Image.Image) -> dict[str, Any]` method.
*   **Return Format:**
    ```python
    {
        "label": "Axial", # or "T1", etc.
        "confidence": 0.985,
        "raw_scores": [...] # optional but recommended for debugging
    }
    ```

### Library & Framework Requirements
*   `onnxruntime`: Use `ort.InferenceSession`.
*   `numpy`: For softmax implementation and array manipulation.
*   `PIL.Image`: As the standard input format for internal consistency.

### File Structure Requirements
*   `src/models/model_plane_cnn.py`
*   `src/models/model_seq_cnn.py`
*   `src/models/model_depth_cnn.py`

### Testing Requirements
*   Create `tests/test_cnn_wrappers.py`.
*   Verify that `predict` returns the expected keys (`label`, `confidence`).
*   Verify confidence score range (0.0 <= x <= 1.0).
*   Mock `onnxruntime.InferenceSession` in tests to avoid needing actual `.onnx` files for unit testing.

## Tasks / Subtasks

- [x] **Implement Plane CNN Wrapper** (AC: #1, #3, #4)
  - [x] Create `src/models/model_plane_cnn.py`
  - [x] Implement `ModelPlaneCNN` with `onnxruntime` and `@st.cache_resource`
  - [x] Implement standard ImageNet-style preprocessing and Softmax postprocessing
- [x] **Implement Sequence CNN Wrapper** (AC: #1, #3, #4)
  - [x] Create `src/models/model_seq_cnn.py`
  - [x] Implement `ModelSeqCNN` class following the same pattern
- [x] **Implement Depth CNN Wrapper** (AC: #1, #3, #4)
  - [x] Create `src/models/model_depth_cnn.py`
  - [x] Implement `ModelDepthCNN` class
- [x] **Author Comprehensive Tests**
  - [x] Create `tests/test_cnn_wrappers.py`
  - [x] Mock `onnxruntime.InferenceSession` for unit tests
  - [x] Verify return format `{"label": str, "confidence": float}` and confidence ranges
- [x] **Final Validation**
  - [x] Run full test suite and verify architectural compliance (Strict Typing)

## Dev Agent Record

### Agent Model Used
Gemini 2.0 Flash

### Debug Log
- (Initial) Story file prepared for development.

### Implementation Plan
- I will start by implementing the `ModelPlaneCNN` wrapper in `src/models/model_plane_cnn.py`.
- Then I'll replicate the pattern for `ModelSeqCNN` and `ModelDepthCNN`.
- Finally, I'll create a single test file `tests/test_cnn_wrappers.py` to verify all three models using mocks.

### Completion Notes
- Implemented `ModelPlaneCNN`, `ModelSeqCNN`, and `ModelDepthCNN` wrappers using `onnxruntime`.
- Integrated `streamlit.cache_resource` for efficient model loading.
- Standardized preprocessing (ImageNet-style) and postprocessing (Softmax for classifiers) across wrappers.
- Created comprehensive unit tests in `tests/test_cnn_wrappers.py` with 100% mock coverage for ONNX sessions.
- All 21 project tests passed.

## File List
- src/models/model_plane_cnn.py
- src/models/model_seq_cnn.py
- src/models/model_depth_cnn.py
- tests/test_cnn_wrappers.py

## Change Log
- (Initial) Created task list and tracking sections.
- (Final) Implemented model wrappers and tests. Updated status to review.

## Status
review
