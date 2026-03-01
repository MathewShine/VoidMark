from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
import os
import uuid
from processor import remove_watermark

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/remove-watermark")
async def process_video(
    video: UploadFile = File(...),
    watermark_text: str = Form(...)
):
    job_id = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_DIR, f"{job_id}_{video.filename}")
    output_path = os.path.join(OUTPUT_DIR, f"{job_id}_clean.mp4")

    with open(input_path, "wb") as f:
        shutil.copyfileobj(video.file, f)

    try:
        success = remove_watermark(input_path, watermark_text, output_path)
        if success and os.path.exists(output_path):
            return FileResponse(
                output_path,
                media_type="video/mp4",
                filename="voidmark_clean.mp4"
            )
        else:
            return {"error": "Processing failed"}
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)

@app.get("/")
def root():
    return {"status": "VoidMark API is running"}