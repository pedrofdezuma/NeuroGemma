import pytest
from src.logic.exceptions import NeuroGemmaError, StageError, ModelTimeoutError, InferenceError

def test_exception_hierarchy():
    """Verify the custom exception hierarchy is correctly implemented."""
    # Test base class
    with pytest.raises(NeuroGemmaError):
        raise NeuroGemmaError("Base error")

    # Test inheritance
    with pytest.raises(NeuroGemmaError):
        raise StageError("Stage error")
    
    with pytest.raises(NeuroGemmaError):
        raise ModelTimeoutError("Timeout error")
    
    with pytest.raises(NeuroGemmaError):
        raise InferenceError("Inference error")

def test_stage_error_properties():
    """Verify StageError can be raised with specific messages."""
    msg = "Pipeline ID stage failed"
    with pytest.raises(StageError) as excinfo:
        raise StageError(msg)
    assert str(excinfo.value) == msg
    assert isinstance(excinfo.value, NeuroGemmaError)
