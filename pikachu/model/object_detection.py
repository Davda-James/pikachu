from ultralytics import YOLO
import cv2
from fastapi import Request
import os 
import glob
import ffmpeg
from collections import defaultdict
import numpy as np

 
def convert_avi_to_mp4_ffmpeg(input_path, output_path):
    ffmpeg.input(input_path).output(output_path, vcodec='libx264', crf=23, preset='medium', acodec='aac', ab='128k').run()


def detect_objects_in_video(model, confidence : float, input_path: str, output_path: str):
    # model.track(
    #     source=input_path,
    #     save=True,
    #     save_txt=False,
    #     stream=False,
    #     verbose=True,
    #     show=False,
    #     project=OUTPUT_DIR,
    #     name="track",
    # )
    # output_avi_files = glob.glob(os.path.join(TRACK_DIR, "*.avi"))
    # print(output_avi_files)
    # if not output_avi_files:
    #     raise FileNotFoundError(f"No AVI file found in {TRACK_DIR}")
    
    # avi_file = output_avi_files[0]
    # convert_avi_to_mp4_ffmpeg(avi_file,output_path)

    # output_mp4_files = glob.glob(os.path.join(TRACK_DIR, "*.mp4"))
    
    # mp4_file = output_mp4_files[0]
    # if os.path.exists(avi_file):
    #     os.remove(avi_file)
    # if os.path.exists(input_path):
    #     os.remove(input_path)
    
    # if not mp4_file:
    #     raise FileNotFoundError(f"No output video found in {avi_file}")

    # return mp4_file 
    

    cap = cv2.VideoCapture(input_path)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_number = 0 
    while True:
        ret, frame = cap.read()
        frame_number += 1
        print(f"Processing frame {frame_number}/{total_frames}")
        if not ret:
            break

        # Run detection or tracking on the frame
        results = model.track(frame, persist=True, verbose=False, stream=False)

        # Draw bounding boxes only
        if results and results[0].boxes is not None:
            for box in results[0].boxes:
                conf = box.conf[0].item()
                if conf < confidence:
                    continue
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        out.write(frame)

    cap.release()
    out.release()

    # Cleanup input
    if os.path.exists(input_path):
        os.remove(input_path)

    return output_path
    

def track_flow(model,confidence : float, input_path: str, output_path: str):# Check CUDA

    cap = cv2.VideoCapture(input_path)

    # Frame info
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Output setup
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    black_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Black background
    cumulative_frame = np.zeros((height, width, 3), dtype=np.uint8)

    # Unique colors
    id_colors = defaultdict(lambda: tuple(np.random.randint(0, 255, size=3).tolist()))

    # Track ID to last position
    id_last_position = {}


    # Run tracking (silent, streamed)
    results = model.track(source=input_path, stream=True, persist=True, conf=confidence, show=False)

    for result in results:
        black_frame = cumulative_frame.copy()

        if result.boxes.id is not None:
            for box, track_id, score in zip(result.boxes.xyxy, result.boxes.id, result.boxes.conf):
                if score.item() < confidence:
                    continue

                x1, y1, x2, y2 = map(int, box.tolist())
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                tid = int(track_id.item())
                color = id_colors[tid]

                # Draw trajectory line
                if tid in id_last_position:
                    last_x, last_y = id_last_position[tid]
                    cv2.line(cumulative_frame, (last_x, last_y), (center_x, center_y), color, 2)

                id_last_position[tid] = (center_x, center_y)

        # Write cumulative frame only (not raw frame)
        black_writer.write(cumulative_frame)

    # Clean up
    cap.release()
    black_writer.release()
    return output_path