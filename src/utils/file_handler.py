"""Utility for handling and validating medical image uploads."""
from io import BytesIO
from typing import Union
from PIL import Image, UnidentifiedImageError

def validate_and_load_image(uploaded_file: Union[BytesIO, any]) -> Image.Image:
    """
    Validates the uploaded file format and content, then loads it as a PIL Image.
    
    Accepts JPG, JPEG, and PNG formats. Performs content-based validation.
    
    Args:
        uploaded_file: The file object uploaded via st.file_uploader.
        
    Returns:
        Image.Image: The validated and loaded PIL Image.
        
    Raises:
        ValueError: If the file format is unsupported or the file is corrupted.
    """
    # 1. Extension check (basic first pass)
    allowed_extensions = {".jpg", ".jpeg", ".png"}
    filename = getattr(uploaded_file, "name", "").lower()
    if not any(filename.endswith(ext) for ext in allowed_extensions):
        raise ValueError(f"Unsupported file format: {filename}. Please upload JPG or PNG.")

    try:
        # 2. Content-based validation
        image = Image.open(uploaded_file)
        
        # Verify the actual format detected by Pillow
        if image.format not in ["JPEG", "PNG"]:
             raise ValueError(f"Unsupported image content: {image.format}. Only JPEG and PNG are allowed.")
        
        # Trigger actual load to check for corruption
        image.load()
        return image
        
    except UnidentifiedImageError:
        raise ValueError("Corrupted or invalid image file. Content does not match recognized image formats.")
    except Exception as e:
        if isinstance(e, ValueError):
            raise e
        raise ValueError(f"Corrupted or invalid image file: {str(e)}")
