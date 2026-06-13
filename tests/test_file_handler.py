import pytest
from io import BytesIO
from PIL import Image
from src.utils.file_handler import validate_and_load_image

def test_validate_and_load_image_valid_jpg():
    # Create a small valid JPEG image in memory
    img = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    
    # We wrap it in a mock object that has a 'name' attribute like a streamlit UploadedFile
    class MockUploadedFile(BytesIO):
        def __init__(self, content, name):
            super().__init__(content)
            self.name = name

    mock_file = MockUploadedFile(img_byte_arr.getvalue(), "test.jpg")
    
    loaded_img = validate_and_load_image(mock_file)
    assert isinstance(loaded_img, Image.Image)
    assert loaded_img.size == (100, 100)

def test_validate_and_load_image_invalid_format():
    mock_file = BytesIO(b"this is not an image")
    mock_file.name = "test.txt"
    
    with pytest.raises(ValueError, match="Unsupported file format"):
        validate_and_load_image(mock_file)

def test_validate_and_load_image_corrupted():
    # JPEG header but random data
    mock_file = BytesIO(b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00`" + b"random junk")
    mock_file.name = "corrupted.jpg"
    
    with pytest.raises(ValueError, match="Corrupted or invalid image file"):
        validate_and_load_image(mock_file)

def test_state_update_integration():
    """Verify how the UI logic would update the state (mocked)."""
    from src.logic.state import InferenceState, PipelineStage
    import streamlit as st
    
    # Create valid image
    img = Image.new('RGB', (100, 100), color='blue')
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    mock_file = BytesIO(img_byte_arr.getvalue())
    mock_file.name = "brain_scan.png"
    
    # Validate
    loaded_img = validate_and_load_image(mock_file)
    
    # Simulate UI update
    inference = InferenceState()
    inference.uploaded_image = loaded_img
    inference.image_metadata = {
        "filename": "brain_scan.png",
        "format": loaded_img.format,
        "size": loaded_img.size
    }
    inference.current_stage = PipelineStage.ID
    
    assert inference.uploaded_image == loaded_img
    assert inference.image_metadata["filename"] == "brain_scan.png"
    assert inference.current_stage == PipelineStage.ID

