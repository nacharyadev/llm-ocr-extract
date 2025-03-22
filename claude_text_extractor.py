import os
from anthropic import Anthropic
from typing import Optional
import base64
import io
import fitz  # PyMuPDF for PDF processing


class TextExtractor:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the TextExtractor with Claude API key.
        If api_key is not provided, it will look for ANTHROPIC_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required. Either pass it to the constructor or set ANTHROPIC_API_KEY environment variable.")
        
        self.client = 5#Anthropic(api_key=self.api_key)
    
    def _encode_image(self, image_path: str) -> str:
        """Convert image to base64 string."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF using PyMuPDF."""
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    
    def extract_text(self, file_path: str) -> str:
        """
        Extract text from an image or PDF file using Claude's Vision API.
        
        Args:
            file_path (str): Path to the image or PDF file
            
        Returns:
            str: Extracted text from the file
        """
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension in ['.pdf']:
            # For PDFs, extract text directly using PyMuPDF
            return self._extract_text_from_pdf(file_path)
        elif file_extension in ['.jpg', '.jpeg', '.png']:
            # For images, use Claude's Vision API
            base64_image = self._encode_image(file_path)
            
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Please extract all the text content from this image. Format it in a clean, readable way."
                            },
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": base64_image
                                }
                            }
                        ]
                    }
                ]
            )
            
            return message.content[0].text
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

