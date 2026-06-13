from streamlit.testing.v1 import AppTest
import pytest
from src.logic.state import PipelineStage
from PIL import Image

def test_download_button_resets_state():
    """
    STORY 4.4 RED PHASE:
    Verify that the download button currently DOES NOT reset the state.
    This test is expected to FAIL after clicking because the callback isn't implemented yet.
    """
    at = AppTest.from_file("app.py", default_timeout=30)
    
    # 1. Setup state
    at.run()
    at.session_state.inference.uploaded_image = Image.new('RGB', (10, 10))
    at.session_state.inference.is_mock_mode = True
    at.run()
    
    # Run mock inference
    mock_btn = [b for b in at.button if b.label == "Load Mock Data"][0]
    mock_btn.click().run()
    
    # Restore uploaded_image (wiped by mock run's reset_state)
    at.session_state.inference.uploaded_image = Image.new('RGB', (10, 10))
    at.run()
    
    assert at.session_state.inference.current_stage == PipelineStage.COMPLETE
    
    # Find the download button. In AppTest, it might be in at.get("download_button")
    # depending on the version. Let's try multiple ways.
    download_btn = None
    
    # Try at.button convenience (sometimes download_button is a button)
    for b in at.button:
        if "Generate Radiology Note" in b.label:
            download_btn = b
            break
            
    if not download_btn:
        # Try generic get
        try:
            download_btns = at.get("download_button")
            if download_btns:
                download_btn = download_btns[0]
        except:
            pass

    if not download_btn:
        # Print what we DO have
        print(f"Buttons: {[b.label for b in at.button]}")
        pytest.fail("Download button not found in AppTest!")
    
    # 2. Click the download button
    download_btn.click().run()
    
    # 3. VERIFY: State should be reset (back to ID stage)
    # CURRENTLY (Red Phase): This should FAIL because on_click is not set
    assert at.session_state.inference.current_stage == PipelineStage.ID, "State was not reset after download!"
