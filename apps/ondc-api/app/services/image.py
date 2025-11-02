from PIL import Image
import io
from typing import Tuple

class ImageService:
    @staticmethod
    def validate_image(file_content: bytes, min_width: int = 800, min_height: int = 800, max_size_mb: int = 2) -> Tuple[bool, str]:
        try:
            if len(file_content) > max_size_mb * 1024 * 1024:
                return False, f"Image size exceeds {max_size_mb}MB"
            
            image = Image.open(io.BytesIO(file_content))
            width, height = image.size
            
            if width < min_width or height < min_height:
                return False, f"Image dimensions must be at least {min_width}x{min_height}px"
            
            return True, "Valid"
        except Exception as e:
            return False, f"Invalid image: {str(e)}"
    
    @staticmethod
    def resize_image(file_content: bytes, max_width: int = 1200, max_height: int = 1200, quality: int = 85) -> bytes:
        try:
            image = Image.open(io.BytesIO(file_content))
            
            image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            output = io.BytesIO()
            image_format = image.format or 'JPEG'
            image.save(output, format=image_format, quality=quality, optimize=True)
            output.seek(0)
            
            return output.read()
        except Exception as e:
            print(f"Error resizing image: {e}")
            return file_content
    
    @staticmethod
    def compress_image(file_content: bytes, quality: int = 85) -> bytes:
        try:
            image = Image.open(io.BytesIO(file_content))
            
            output = io.BytesIO()
            image_format = image.format or 'JPEG'
            image.save(output, format=image_format, quality=quality, optimize=True)
            output.seek(0)
            
            return output.read()
        except Exception as e:
            print(f"Error compressing image: {e}")
            return file_content

image_service = ImageService()
