# VoidMark 

> **AI-powered watermark removal tool for short videos**  
> Upload. Erase. Download. Clean.

---

## What is VoidMark?

VoidMark is a web-based tool that lets you remove text watermarks from videos — automatically. You upload a video, tell it what text to remove, and it returns a clean version with the watermark erased using AI inpainting.

No manual editing. No Photoshop. Just paste the text and go.

---

## Features

-  Supports short videos (8–10 seconds, MP4/MOV/AVI)
-  Auto-detects watermark position using OCR
-  Removes watermark using OpenCV inpainting
-  Preserves original audio track
-  Instant download of processed video
-  Clean, minimal single-page UI

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| OCR | EasyOCR |
| Video Processing | OpenCV, FFmpeg |
| Packaging | Uvicorn |

---

## Project Structure

```
voidmark/
├── backend/
│   ├── main.py            # FastAPI server & API routes
│   ├── processor.py       # OCR detection + inpainting logic
│   ├── uploads/           # Temp uploaded video storage
│   └── outputs/           # Processed video output
├── frontend/
│   └── index.html         # Single-page UI
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

```bash
# Install FFmpeg (required for video processing)
sudo apt install ffmpeg        # Linux
brew install ffmpeg            # macOS
```

### Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/voidmark.git
cd voidmark

# Install Python dependencies
pip install -r requirements.txt
```

### Run the App

```bash
# Start the backend server
cd backend
uvicorn main:app --reload --port 8000
```

Then open `frontend/index.html` in your browser — or serve it:

```bash
cd frontend
python -m http.server 3000
```

Visit: `http://localhost:3000`

---

## How It Works

```
1. User uploads video + enters watermark text
       ↓
2. Video is split into frames using FFmpeg
       ↓
3. EasyOCR scans frames to locate the watermark region
       ↓
4. OpenCV inpainting fills in the detected region
       ↓
5. Frames are reassembled + audio restored via FFmpeg
       ↓
6. Processed video is returned for download
```

---

## Requirements

```txt
fastapi
uvicorn
python-multipart
opencv-python-headless
easyocr
numpy
pillow
```

Install all:

```bash
pip install -r requirements.txt
```

---

## Limitations

- Optimized for videos up to 10 seconds
- Works best with static/fixed-position watermarks
- Text must be readable (not heavily stylized or transparent)
- Processing time: ~15–60 seconds depending on system

