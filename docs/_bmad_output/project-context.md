---
project_name: 'NeuroGemma'
user_name: 'Pedro'
date: '2026-05-11'
sections_completed: ['technology_stack', 'language_rules', 'framework_rules', 'testing_rules', 'quality_rules', 'workflow_rules', 'anti_patterns']
status: 'complete'
rule_count: 29
optimized_for_llm: true
existing_patterns_found: 5
---

# Project Context for AI Agents

_This file contains critical rules and patterns that AI agents must follow when implementing code in this project. Focus on unobvious details that agents might otherwise miss._

---

## Technology Stack & Versions

- **Core Runtime:** Python 3.12 (Conda)
- **Frontend/Orchestration:** Streamlit
- **Inference:** ONNX Runtime (CNNs), Transformers (4-bit MedGemma VLM)
- **Reporting:** fpdf2
- **Testing:** Pytest
- **Infrastructure:** Docker with NVIDIA-container-toolkit

## Critical Implementation Rules

### Language-Specific Rules (Python 3.12)

- **Strict Type Hinting:** Mandatory use of type hints for all function signatures and complex state objects.
- **Explicit Resource Cleanup:** Use context managers for file I/O and temporary report artifacts.
- **Structured Logging:** Use `logging` for all pipeline events; do not use `print()` for production logic.
- **Custom Error Hierarchy:** Implement stage-specific exceptions derived from a base `NeuroGemmaError` to support granular UI feedback.

### Framework-Specific Rules (Streamlit)

- **Centralized Pipeline State:** All workflow state must reside in a structured `st.session_state.inference` object (using an `InferenceState` dataclass).
- **Global Model Hub:** AI models must be loaded via `@st.cache_resource` to prevent redundant memory allocation.
- **UI Decoupling:** Keep the "Diagnostic View" and "Technical Logs" strictly separated into tabs or containers to ensure clinical clarity.
- **UX Feedback:** Use `st.status` or `st.progress` during all inference stages; provide human-readable feedback for the MedGemma thought process.

### Testing Rules (Pytest)

- **Pure-Logic Testing:** Test all pipeline orchestration logic (Logic Gate) independently of AI model weights using static mocks.
- **Inference Mocking:** Mandatory use of fixtures to simulate heterogeneous model outputs (CNN classes and VLM strings).
- **Report Validation:** Implement automated checks for PDF generation success and basic metadata/content presence.
- **Environment Agnostic:** Tests must be runnable on Windows/MacOS without a GPU by default; use `@pytest.mark.gpu` to isolate live model tests.

### Code Quality & Style Rules

- **Naming Conventions:**
  - Files: `snake_case.py`
  - Classes: `PascalCase`
  - Functions/Variables: `snake_case`
  - AI Models: Prefix with `model_` (e.g., `model_axial_cnn`)
- **Documentation:** Every module must have a docstring explaining its role in the clinical pipeline. Use Google-style docstrings.
- **Modular Monolith:** No UI logic (`st.xxx`) should ever exist inside `src/logic/` or `src/models/`.

### Development Workflow Rules

- **Branch Naming:** `feature/`, `fix/`, or `research/` prefixes.
- **Commit Messages:** Follow Conventional Commits (e.g., `feat(logic): add Axial-Flair logic gate rules`).
- **Mock-First Development:** Implementation of new pipeline stages must start with a Mock Mode variant before live model integration.

### Critical Don't-Miss Rules (Anti-Patterns)

- **NO External APIs:** Never attempt to use OpenAI, Anthropic, or other cloud APIs; all inference must remain local.
- **NO Session Bloat:** Do not store large objects (images, model weights) directly in `st.session_state`. Store them as file paths or use `@st.cache_resource`.
- **Mandatory Privacy Reset:** Every route to "Report Download" must be followed by a clear signal to wipe the current `InferenceState`.
- **Latency Awareness:** If a model takes >10s, it MUST have a granular progress update or status message.

---

## Usage Guidelines

**For AI Agents:**

- Read this file before implementing any code.
- Follow ALL rules exactly as documented.
- When in doubt, prefer the more restrictive option.
- Update this file if new patterns emerge.

**For Humans:**

- Keep this file lean and focused on agent needs.
- Update when technology stack changes.
- Review quarterly for outdated rules.
- Remove rules that become obvious over time.

Last Updated: 2026-05-11
