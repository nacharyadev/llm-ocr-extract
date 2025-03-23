from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
from typing import List, Optional
import shutil
from claude_text_extractor import TextExtractor
from google_text_extractor import GoogleVisionTextExtractor
from openai_text_extractor import OpenAIVisionTextExtractor
from purchase_orders import PurchaseOrder, PurchaseOrderList, parse_purchase_order

app = FastAPI()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Get API keys from environment variables
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print(GEMINI_API_KEY)
# Initialize text extractors with API keys
#claude_extractor = TextExtractor(api_key=ANTHROPIC_API_KEY)
google_extractor = GoogleVisionTextExtractor(api_key=GEMINI_API_KEY)
#penai_extractor = OpenAIVisionTextExtractor(api_key=OPENAI_API_KEY)

# Allowed file types
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/jpg"]
ALLOWED_PDF_TYPES = ["application/pdf"]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"good morning {name}! How are you doing today?"}

@app.post("/upload/image/claude")
async def upload_image_claude(file: UploadFile = File(...)):
    if not ANTHROPIC_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Claude API key not configured. Please set ANTHROPIC_API_KEY environment variable."
        )
    
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_IMAGE_TYPES)}"
        )
    
    try:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
        
        extracted_text = claude_extractor.extract_text(file_location)
        
        return JSONResponse(
            content={
                "message": "File uploaded and processed successfully",
                "filename": file.filename,
                "content_type": file.content_type,
                "file_size": os.path.getsize(file_location),
                "extracted_text": extracted_text,
                "extractor": "claude"
            },
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload/image/google")
async def upload_image_google(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_IMAGE_TYPES)}"
        )
    
    try:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
        
        extracted_text = google_extractor.extract_text(file_location)
        print(extracted_text)
        purchase_order: Optional[PurchaseOrder] = parse_purchase_order(extracted_text)
        print(purchase_order)
        if purchase_order:
            purchase_order = PurchaseOrderList().get_purchase_order(purchase_order.purchaseOrderNumber)
            print(purchase_order)
        
        return JSONResponse(
            content={
                "message": "File uploaded and processed successfully",
                "filename": file.filename,
                "content_type": file.content_type,
                "file_size": os.path.getsize(file_location),
                "extracted_text": extracted_text,
                "extractor": "google",
                "purchase_order": purchase_order.to_dict() if purchase_order else None
            },
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload/image/openai")
async def upload_image_openai(file: UploadFile = File(...)):
    if not OPENAI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
        )
    
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_IMAGE_TYPES)}"
        )
    
    try:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
        
        extracted_text = openai_extractor.extract_text(file_location)
        
        return JSONResponse(
            content={
                "message": "File uploaded and processed successfully",
                "filename": file.filename,
                "content_type": file.content_type,
                "file_size": os.path.getsize(file_location),
                "extracted_text": extracted_text,
                "extractor": "openai"
            },
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_PDF_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_PDF_TYPES)}"
        )
    
    try:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
        
        # Use any extractor for PDFs since they all use PyMuPDF
        extracted_text = claude_extractor.extract_text(file_location)
        
        return JSONResponse(
            content={
                "message": "File uploaded and processed successfully",
                "filename": file.filename,
                "content_type": file.content_type,
                "file_size": os.path.getsize(file_location),
                "extracted_text": extracted_text,
                "extractor": "pymupdf"
            },
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)