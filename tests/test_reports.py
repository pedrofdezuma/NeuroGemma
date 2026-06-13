import pytest
from src.logic.state import InferenceState, PipelineStage
from src.reports.report_engine import RadiologyReport, generate_report, get_report_filename
from PIL import Image
import io
import os

@pytest.fixture
def mock_inference_state():
    """Provides a fully populated InferenceState for testing."""
    state = InferenceState()
    state.current_stage = PipelineStage.COMPLETE
    state.results = {
        "plane": "Axial",
        "sequence": "FLAIR",
        "depth": "120",
        "plane_confidence": 0.98,
        "sequence_confidence": 0.95,
        "depth_confidence": 0.92,
        "narrative": "Hyperintense lesions observed in the periventricular white matter, consistent with multiple sclerosis. No significant mass effect or midline shift."
    }
    # Create a small mock image
    img = Image.new('RGB', (100, 100), color='red')
    state.uploaded_image = img
    state.image_metadata = {"filename": "test_scan.jpg"}
    return state

def test_radiology_report_header_footer():
    """Verify that the RadiologyReport base class includes header and footer elements."""
    pdf = RadiologyReport()
    pdf.add_page()
    output = pdf.output()
    assert len(output) > 0

def test_generate_report_output_type(mock_inference_state):
    """Confirm generate_report returns a byte-like stream."""
    pdf_bytes = generate_report(mock_inference_state)
    assert isinstance(pdf_bytes, (bytes, bytearray))
    assert len(pdf_bytes) > 0

def test_generate_report_content(mock_inference_state):
    """Basic check to see if key strings exist in the PDF output."""
    # Disable compression so we can search for strings in the byte stream
    pdf_bytes = generate_report(mock_inference_state, compress=False)
    # Search in bytes to avoid encoding issues
    assert b"Radiology Note" in pdf_bytes
    assert b"Axial" in pdf_bytes
    assert b"FLAIR" in pdf_bytes
    assert b"Hyperintense lesions" in pdf_bytes
    assert b"AI-generated draft" in pdf_bytes
    assert b"Validated by" in pdf_bytes

def test_get_report_filename(mock_inference_state):
    """Verify the naming convention for report files."""
    filename = get_report_filename(mock_inference_state)
    # Convention: {original_filename}_{plane}_{timestamp}.pdf
    assert filename.startswith("test_scan_axial_")
    assert filename.endswith(".pdf")
    # Check timestamp part (approximate length check)
    assert len(filename) == len("test_scan_axial_YYYYMMDDHHMM.pdf")
