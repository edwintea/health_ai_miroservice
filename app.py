import os
import logging
import torch
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
from PIL import Image
from io import BytesIO

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Mouth Cancer Detection API",
    description="API backend for mouth cancer detection using Hugging Face model.",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Hugging Face image classification pipeline with the specified model
device = "cuda" if torch.cuda.is_available() else "cpu"
classifier = pipeline("image-classification", model="google/vit-base-patch16-224", use_fast=True, device=device)

@app.get("/")
async def root():
    return {"message": "Welcome to the Mouth Cancer Detection API. Use POST /api/inference with an image file."}

@app.post("/api/inference")
async def inference_endpoint(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    # Read file bytes
    file_bytes = await file.read()

    # Convert image bytes to a format suitable for the classifier
    try:
        image = Image.open(BytesIO(file_bytes))
    except Exception as e:
        logger.error("Error processing image: %s", str(e))
        raise HTTPException(status_code=400, detail="Error processing image.")

    try:
        # Call the classifier
        predictions = classifier(image)

        # Format predictions for the response
        formatted_predictions = [
            {"label": pred["label"], "score": pred["score"]}
            for pred in predictions
        ]
    except Exception as e:
        logger.error("Inference error: %s", str(e))
        raise HTTPException(status_code=500, detail="Inference error. Please try again later.")

    return {
        "filename": file.filename,
        "predictions": formatted_predictions
    }
