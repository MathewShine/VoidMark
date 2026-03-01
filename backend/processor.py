import cv2
import numpy as np
import easyocr
import os
import subprocess
import tempfile
import shutil

FFMPEG = r"C:\Users\cores\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe"
FFPROBE = r"C:\Users\cores\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffprobe.exe"

reader = easyocr.Reader(['en'], gpu=False)

def remove_watermark(video_path: str, watermark_text: str, output_path: str):
    temp_dir = tempfile.mkdtemp()
    frames_dir = os.path.join(temp_dir, "frames")
    output_frames_dir = os.path.join(temp_dir, "output_frames")
    os.makedirs(frames_dir)
    os.makedirs(output_frames_dir)

    try:
        subprocess.run([
            FFMPEG, "-i", video_path,
            os.path.join(frames_dir, "frame_%04d.png"), "-y"
        ], check=True, capture_output=True)

        audio_path = os.path.join(temp_dir, "audio.aac")
        subprocess.run([
            FFMPEG, "-i", video_path,
            "-vn", "-acodec", "copy", audio_path, "-y"
        ], capture_output=True)

        frames = sorted([f for f in os.listdir(frames_dir) if f.endswith(".png")])

        first_frame = cv2.imread(os.path.join(frames_dir, frames[0]))
        region = detect_text_region(first_frame, watermark_text)

        for frame_file in frames:
            frame = cv2.imread(os.path.join(frames_dir, frame_file))
            if region:
                frame = inpaint_region(frame, region)
            cv2.imwrite(os.path.join(output_frames_dir, frame_file), frame)

        result = subprocess.run([
            FFPROBE, "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=r_frame_rate",
            "-of", "default=noprint_wrappers=1:nokey=1", video_path
        ], capture_output=True, text=True)
        fps = eval(result.stdout.strip()) if result.stdout.strip() else 30

        temp_video = os.path.join(temp_dir, "temp_video.mp4")
        subprocess.run([
            FFMPEG, "-framerate", str(fps),
            "-i", os.path.join(output_frames_dir, "frame_%04d.png"),
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            temp_video, "-y"
        ], check=True, capture_output=True)

        if os.path.exists(audio_path):
            subprocess.run([
                FFMPEG, "-i", temp_video, "-i", audio_path,
                "-c:v", "copy", "-c:a", "aac",
                "-shortest", output_path, "-y"
            ], check=True, capture_output=True)
        else:
            shutil.copy(temp_video, output_path)

        return True

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def detect_text_region(frame, target_text: str):
    results = reader.readtext(frame)
    target_lower = target_text.lower().strip()
    for (bbox, text, confidence) in results:
        if target_lower in text.lower():
            xs = [int(p[0]) for p in bbox]
            ys = [int(p[1]) for p in bbox]
            padding = 10
            x1 = max(0, min(xs) - padding)
            y1 = max(0, min(ys) - padding)
            x2 = min(frame.shape[1], max(xs) + padding)
            y2 = min(frame.shape[0], max(ys) + padding)
            return (x1, y1, x2, y2)
    return None


def inpaint_region(frame, region):
    x1, y1, x2, y2 = region
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    mask[y1:y2, x1:x2] = 255
    result = cv2.inpaint(frame, mask, inpaintRadius=5, flags=cv2.INPAINT_TELEA)
    return result