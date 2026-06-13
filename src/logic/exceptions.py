"""
Custom exception hierarchy for the NeuroGemma clinical pipeline.
Derived from a base NeuroGemmaError to support granular UI feedback and structured logging.
"""

class NeuroGemmaError(Exception):
    """Base exception for all NeuroGemma-related errors."""
    pass

class StageError(NeuroGemmaError):
    """Exception raised for failures in specific pipeline stages (ID, GATE, SYNTHESIS)."""
    pass

class ModelTimeoutError(NeuroGemmaError):
    """Exception raised when an AI model exceeds latency limits (simulated or real)."""
    pass

class InferenceError(NeuroGemmaError):
    """Exception raised for general model inference failures."""
    pass
