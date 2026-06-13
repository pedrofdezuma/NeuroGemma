# NeuroGemma Project Mandates

## Development Workflow

- **Primary Environment:** Conda is the preferred environment for local development.
- **Environment Name:** `neuro_env`
- **Dependency Management:** Maintain `environment.yml` as the source of truth for dependencies.

## Implementation Standards

- **Strict Typing:** All Python code must use explicit type hints.
- **Modular Monolith:** Maintain strict separation between UI (`app.py`), logic (`src/logic`), and models (`src/models`).
- **Local Inference:** No external AI APIs allowed. All models must run locally.
