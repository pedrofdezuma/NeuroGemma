# Story 2.3: MedGemma VLM Wrapper (4-bit Quantized)

Status: review

## Story

As a Developer,
I want to implement a wrapper for the MedGemma VLM using 4-bit quantization,
so that I can generate high-quality clinical narratives on local GPU memory.

## Acceptance Criteria

1. **Given** a triggered VLM inference request
2. **When** the model processes the image
3. **Then** it generates a raw natural language narrative
4. **And** the narrative generation completes within 60 seconds
5. **And** the model is loaded using **real weights** via 4-bit quantization (`BitsAndBytesConfig`) to fit in local GPU memory
6. **And** the wrapper follows the established project pattern (`predict(self, image: Image.Image) -> dict[str, Any]`)

## Tasks / Subtasks

- [x] **Implement MedGemma VLM Wrapper** (AC: #1, #2, #3, #5, #6)
  - [x] Create `src/models/model_medgemma_vlm.py`
  - [x] Implement `ModelMedGemmaVLM` class using `transformers` and `bitsandbytes`
  - [x] Configure `BitsAndBytesConfig` for 4-bit quantization (`load_in_4bit=True`, `bnb_4bit_quant_type="nf4"`)
  - [x] Implement `@st.cache_resource` for efficient model and processor loading
  - [x] Implement `predict(self, image: Image.Image)` method returning `{"label": "Narrative", "text": str}`
- [x] **Author Comprehensive Tests** (AC: #4, #6)
  - [x] Create `tests/test_vlm_wrapper.py`
  - [x] Mock `transformers.PaliGemmaForConditionalGeneration` and `transformers.PaliGemmaProcessor` for unit testing logic
  - [x] Verify that `predict` returns the expected dictionary structure and text
  - [x] Ensure `BitsAndBytesConfig` is correctly instantiated during model loading

## Dev Notes

- **Frameworks:** `transformers`, `bitsandbytes`, `accelerate`, `torch`.
- **Real Weights:** The implementation must use `from_pretrained` to load the actual model (e.g., `google/paligemma-3b-pt-224` or the specific MedGemma fine-tune).
- **Quantization:** 4-bit NormalFloat (NF4) with double quantization is mandatory to ensure the model runs on the local research server.
- **Pattern:** Each model wrapper in `src/models/` must be a self-contained unit handling its own weights and preprocessing.
- **State Integration:** This wrapper will be called by the `LogicGate` (Story 2.4).
- **InferenceState:** The output should eventually be stored in `InferenceState.results["narrative"]`.

### Project Structure Notes

- **File Path:** `src/models/model_medgemma_vlm.py`
- **Class Name:** `ModelMedGemmaVLM`
- **Testing:** `tests/test_vlm_wrapper.py`
- **Consistency:** Follows the `model_{name}_{type}.py` naming convention established in the Architecture Decision Document.

### References

- **Architecture:** `docs/_bmad_output/planning-artifacts/architecture.md#Naming Patterns`
- **Epics:** `docs/_bmad_output/planning-artifacts/epics.md#Story 2.3: MedGemma VLM Wrapper (4-bit Quantized)`
- **Previous Work:** `docs/_bmad_output/implementation-artifacts/2-2-cnn-model-wrappers-onnx.md` (for structural pattern)

## Dev Agent Record

### Agent Model Used

Gemini 2.0 Flash (via Gemini CLI)

### Debug Log References
- Initialized story development.
- Implemented `ModelMedGemmaVLM` with 4-bit quantization using `bitsandbytes`.
- Discovered and resolved Streamlit cache interference in unit tests by using unique model IDs.
- Verified implementation with comprehensive mocks.

### Completion Notes List
- Successfully implemented `ModelMedGemmaVLM` in `src/models/model_medgemma_vlm.py`.
- Verified 4-bit quantization config (NF4, double quant, bfloat16).
- Achieved 100% test pass rate for the new wrapper.

### File List
- src/models/model_medgemma_vlm.py
- tests/test_vlm_wrapper.py

