import pytest
import numpy as np
from PIL import Image
from unittest.mock import MagicMock, patch
import src.models.model_plane_cnn as plane_module
from src.models.model_plane_cnn import ModelPlaneCNN
from src.models.model_seq_cnn import ModelSeqCNN
from src.models.model_depth_cnn import ModelDepthCNN

@pytest.fixture(autouse=True)
def clear_streamlit_cache():
    """Clear streamlit cache before each test to avoid cross-test contamination."""
    plane_module.load_onnx_session.clear()

@pytest.fixture
def dummy_image():
    return Image.fromarray(np.uint8(np.random.rand(224, 224, 3) * 255))

@patch("os.path.exists")
def test_model_plane_cnn_predict_format(mock_exists, dummy_image):
    """Verify that ModelPlaneCNN.predict returns the correct dictionary format."""
    mock_exists.return_value = True
    with patch("onnxruntime.InferenceSession") as mock_session_class:
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        
        mock_input = MagicMock()
        mock_input.name = "input"
        mock_session.get_inputs.return_value = [mock_input]
        
        # Logits that result in a clear winner after softmax
        # Index 2 is sagittal
        mock_session.run.return_value = [np.array([[0.0, 0.0, 10.0, 0.0]], dtype=np.float32)]
        
        model = ModelPlaneCNN(model_path="plane.onnx")
        result = model.predict(dummy_image)
        
        assert isinstance(result, dict)
        assert result["label"] == "sagittal"
        assert result["confidence"] > 0.99
        assert len(result["raw_scores"]) == 4

@patch("os.path.exists")
def test_model_seq_cnn_predict_format(mock_exists, dummy_image):
    """Verify that ModelSeqCNN.predict returns the correct dictionary format."""
    mock_exists.return_value = True
    with patch("onnxruntime.InferenceSession") as mock_session_class:
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        
        mock_input = MagicMock()
        mock_input.name = "input"
        mock_session.get_inputs.return_value = [mock_input]
        
        # Index 3 is flair
        mock_session.run.return_value = [np.array([[0.0, 0.0, 0.0, 10.0, 0.0]], dtype=np.float32)]
        
        model = ModelSeqCNN(model_path="seq.onnx")
        result = model.predict(dummy_image)
        
        assert isinstance(result, dict)
        assert result["label"].lower() == "flair"
        assert result["confidence"] > 0.99
        assert len(result["raw_scores"]) == 5

@patch("os.path.exists")
def test_model_depth_cnn_predict_format(mock_exists, dummy_image):
    """Verify that ModelDepthCNN.predict returns the correct dictionary format."""
    mock_exists.return_value = True
    with patch("onnxruntime.InferenceSession") as mock_session_class:
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        
        mock_input = MagicMock()
        mock_input.name = "input"
        mock_session.get_inputs.return_value = [mock_input]
        
        mock_session.run.return_value = [np.array([[[0.456]]], dtype=np.float32)]
        
        model = ModelDepthCNN(model_path="depth.onnx")
        result = model.predict(dummy_image)
        
        assert isinstance(result, dict)
        assert result["label"] == pytest.approx(0.456)
        assert result["confidence"] == 1.0
        assert result["raw_scores"][0] == pytest.approx(0.456)

@patch("os.path.exists")
def test_model_depth_cnn_rotation(mock_exists, dummy_image):
    """Verify that ModelDepthCNN rotates the image when filename starts with 'brats-'."""
    mock_exists.return_value = True
    with patch("onnxruntime.InferenceSession") as mock_session_class:
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        
        mock_input = MagicMock()
        mock_input.name = "input"
        mock_session.get_inputs.return_value = [mock_input]
        mock_session.run.return_value = [np.array([[[0.5]]], dtype=np.float32)]

        model = ModelDepthCNN(model_path="depth.onnx")
        
        # Test with brats- filename
        with patch.object(Image.Image, 'transpose', wraps=dummy_image.transpose) as mock_transpose:
            model.predict(dummy_image, filename="brats-001.png")
            # Image.ROTATE_270 is 90 degrees clockwise
            mock_transpose.assert_any_call(Image.ROTATE_270)
        
        # Test without brats- filename
        with patch.object(Image.Image, 'transpose', wraps=dummy_image.transpose) as mock_transpose:
            model.predict(dummy_image, filename="normal-001.png")
            # Should NOT call transpose with ROTATE_270
            for call in mock_transpose.call_args_list:
                assert call.args[0] != Image.ROTATE_270

