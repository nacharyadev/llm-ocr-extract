import os
from typing import Optional
import base64
import io
import fitz  # PyMuPDF for PDF processing
from google import genai
from google.genai import types
import requests


class GoogleVisionTextExtractor:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the GoogleVisionTextExtractor with Gemini API key.
        If api_key is not provided, it will look for GOOGLE_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required. Either pass it to the constructor or set GOOGLE_API_KEY environment variable.")
        
        self.client = genai.Client(api_key=self.api_key)
    
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
        Extract text from an image or PDF file using Google's Gemini API.
        
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
            # For images, use Gemini API
            with open(file_path, "rb") as image_file:
                image_data = image_file.read()
            
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=[
                    """Extract all the text content from the attached image of a packing slip. Return the result in a strict JSON format:
                    
                    Use this JSON schema:
                    Item = {'itemName': str, 'itemQuantity': int, 'itemPrice': float}
                    PackingSlip = {'trackingNumber': str, 'date': str, 'customerName': str, 'customerAddress': str, 'purchaseOrderNumber': str, 'items': list[Item]}
                    Return: PackingSlip
                    """,
                    types.Part.from_bytes(data=image_data, mime_type=f"image/{file_extension[1:]}")
                ]
            )
            
            return response.text
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")