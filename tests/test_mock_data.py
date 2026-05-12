import pytest
from src.utils.mock_data import get_mock_results, GOLDEN_DATASETS

def test_get_mock_results_axial_flair():
    """Test that Axial-FLAIR mock results are correctly retrieved."""
    results = get_mock_results("axial_flair")
    assert results["plane"] == "Axial"
    assert results["sequence"] == "FLAIR"
    assert "Positive for hyperintense signal" in results["narrative"]

def test_get_mock_results_sagittal_t1():
    """Test that Sagittal-T1 mock results are correctly retrieved."""
    results = get_mock_results("sagittal_t1")
    assert results["plane"] == "Sagittal"
    assert results["sequence"] == "T1"
    assert results["narrative"] is None

def test_get_mock_results_invalid_id():
    """Test that an invalid dataset ID raises a ValueError."""
    with pytest.raises(ValueError, match="Unknown dataset ID"):
        get_mock_results("invalid_id")

def test_golden_datasets_keys():
    """Test that the expected keys are in GOLDEN_DATASETS."""
    assert "axial_flair" in GOLDEN_DATASETS
    assert "sagittal_t1" in GOLDEN_DATASETS
