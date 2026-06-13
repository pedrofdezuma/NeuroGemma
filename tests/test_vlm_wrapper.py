import pytest
from unittest.mock import MagicMock, patch
from PIL import Image
import torch
from src.models.model_medgemma_vlm import ModelMedGemmaVLM

@pytest.fixture
def mock_image():
    return Image.new("RGB", (224, 224), color="white")

@patch("src.models.model_medgemma_vlm.BitsAndBytesConfig")
@patch("src.models.model_medgemma_vlm.PaliGemmaForConditionalGeneration.from_pretrained")
@patch("src.models.model_medgemma_vlm.PaliGemmaProcessor.from_pretrained")
def test_vlm_model_loading(mock_processor_load, mock_model_load, mock_bnb_config):
    """Test if the model and processor are loaded with the correct configuration."""
    # Setup mocks
    mock_model = MagicMock()
    mock_model_load.return_value = mock_model
    mock_processor = MagicMock()
    mock_processor_load.return_value = mock_processor
    
    # Instantiate model (this should trigger loading)
    model_wrapper = ModelMedGemmaVLM(model_id="mock/model_loading")
    
    # Verify BitsAndBytesConfig was called with correct parameters
    mock_bnb_config.assert_called_once_with(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16
    )
    
    # Verify model loading parameters
    mock_model_load.assert_called_once()
    args, kwargs = mock_model_load.call_args
    assert kwargs["quantization_config"] == mock_bnb_config.return_value
    assert kwargs["device_map"] == "auto"

@patch("src.models.model_medgemma_vlm.PaliGemmaForConditionalGeneration.from_pretrained")
@patch("src.models.model_medgemma_vlm.PaliGemmaProcessor.from_pretrained")
def test_vlm_predict(mock_processor_load, mock_model_load, mock_image):
    """Test the predict method returns the expected structure."""
    # Setup model mock
    mock_model = MagicMock()
    mock_model.device = "cpu"
    mock_model.generate.return_value = torch.tensor([[1, 2, 3, 4]])
    mock_model_load.return_value = mock_model
    
    # Setup processor mock
    mock_processor = MagicMock()
    # Mock the __call__ method to return something with a .to() method
    mock_inputs = MagicMock()
    mock_inputs.__getitem__.return_value = torch.tensor([[1, 2]]) # for input_ids.shape[-1]
    mock_processor.return_value = mock_inputs
    mock_processor.batch_decode.return_value = ["Generated clinical narrative"]
    mock_processor_load.return_value = mock_processor
    
    model_wrapper = ModelMedGemmaVLM(model_id="mock/model_predict")
    result = model_wrapper.predict(mock_image)
    
    assert result["label"] == "Narrative"
    assert result["text"] == "Generated clinical narrative"
    assert isinstance(result["text"], str)

@patch("src.models.model_medgemma_vlm.load_vlm_model")
def test_vlm_load_failure(mock_load):
    """Test behavior when the model fails to load."""
    mock_load.side_effect = Exception("GPU out of memory")
    
    model_wrapper = ModelMedGemmaVLM(model_id="mock/failure")
    result = model_wrapper.predict(Image.new("RGB", (10, 10)))
    
    assert result["label"] == "Narrative"
    assert "Model not loaded" in result["text"]
