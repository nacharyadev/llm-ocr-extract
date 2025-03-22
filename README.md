# FastAPI Hello World

A simple Hello World REST API built with FastAPI with file upload and text extraction capabilities using multiple Vision APIs (Claude, Google Cloud Vision, and OpenAI).

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API keys:
```bash
# For Claude API
export ANTHROPIC_API_KEY='your-claude-api-key-here'

# For Google Cloud Vision API
export GOOGLE_APPLICATION_CREDENTIALS='path/to/your/google-credentials.json'

# For OpenAI API
export OPENAI_API_KEY='your-openai-api-key-here'
```

## Running the Application

Start the server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Available Endpoints

- `GET /`: Returns a simple "Hello World" message
- `GET /hello/{name}`: Returns a personalized hello message
- `POST /upload/image/claude`: Upload an image and extract text using Claude's Vision API
- `POST /upload/image/google`: Upload an image and extract text using Google Cloud Vision API
- `POST /upload/image/openai`: Upload an image and extract text using OpenAI's Vision API
- `POST /upload/pdf`: Upload a PDF file and extract text using PyMuPDF

## File Upload and Text Extraction

### Upload an Image and Extract Text with Claude
```bash
curl -X POST -F "file=@/path/to/your/image.jpg" http://localhost:8000/upload/image/claude
```

Gemini setup: https://ai.google.dev/gemini-api/docs/vision?lang=python
### Upload an Image and Extract Text with Google Gemini API:
```bash
curl -X POST -F "file=@/path/to/your/image.jpg" http://localhost:8000/upload/image/google
```

### Upload an Image and Extract Text with OpenAI
```bash
curl -X POST -F "file=@/path/to/your/image.jpg" http://localhost:8000/upload/image/openai
```

### Upload a PDF and Extract Text
```bash
curl -X POST -F "file=@/path/to/your/document.pdf" http://localhost:8000/upload/pdf
```

### Allowed File Types
- Images: JPEG, PNG, JPG
- Documents: PDF

### Response Format
The API will return a JSON response with:
- File metadata (filename, content type, file size)
- Extracted text content
- Success/error message
- Extractor used (claude, google, openai, or pymupdf)

## API Documentation

Once the server is running, you can access:
- Interactive API docs (Swagger UI): `http://localhost:8000/docs`
- Alternative API docs (ReDoc): `http://localhost:8000/redoc`

## File Storage

Uploaded files are stored in the `uploads` directory in your project folder. Make sure this directory has appropriate write permissions.

## Dependencies

- FastAPI: Web framework
- Uvicorn: ASGI server
- Anthropic: Claude API client
- Google Cloud Vision: Google's Vision API client
- OpenAI: OpenAI API client
- PyMuPDF: PDF text extraction
- Python-multipart: File upload handling

## Environment Variables

- `ANTHROPIC_API_KEY`: Your Anthropic API key for Claude's Vision API
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to your Google Cloud credentials JSON file
- `OPENAI_API_KEY`: Your OpenAI API key for Vision API

Deactivate and reinstall:
```bash
deactivate 2>/dev/null || true && source ./venv/bin/activate && which python && pip install -r requirements.txt
```