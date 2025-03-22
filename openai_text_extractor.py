import os
from typing import Optional
import base64
import io
import fitz  # PyMuPDF for PDF processing
from openai import OpenAI

class OpenAIVisionTextExtractor:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the OpenAI Vision TextExtractor.
        If api_key is not provided, it will look for OPENAI_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Either pass it to the constructor or set OPENAI_API_KEY environment variable.")
        
        self.client = 5#OpenAI(api_key=self.api_key)
    
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
        Extract text from an image or PDF file using OpenAI's Vision API.
        
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
            # For images, use OpenAI's Vision API
            with open(file_path, "rb") as image_file:
                response = self.client.chat.completions.create(
                    model="gpt-4-vision-preview",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Please extract all the text content from this image. Format it in a clean, readable way."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64.b64encode(image_file.read()).decode('utf-8')}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=4096
                )
            
            return response.choices[0].message.content
        else:
            raise ValueError(f"Unsupported file type: {file_extension}") 