from ultralytics import YOLO
import cv2
from fastapi import Request
import os 
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
    if not cap.isOpened():
        raise RuntimeError("Failed to open video file")

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
        results = model.track(frame, persist=True, conf=confidence, verbose=False, stream=False)

        # Draw bounding boxes only
        if results and results[0].boxes is not None:
            for box in results[0].boxes:
                conf = box.conf[0].item()
                # if conf < confidence:
                #     continue
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

    if not cap.isOpened():
        raise ValueError(f"[ERROR] Could not open video file: {input_path}")

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
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    for result in results:
        black_frame = cumulative_frame.copy()

        if result.boxes.id is not None:
            for box, track_id, score in zip(result.boxes.xyxy, result.boxes.id, result.boxes.conf):
                # if score.item() < confidence:
                #     continue

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
    
    if os.path.exists(input_path):
        os.remove(input_path)

    return output_path

def track_overlay(model,confidence : float, input_path: str, output_path: str):
    cap = cv2.VideoCapture(input_path)

    # Frame size
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # or 'XVID', 'avc1' depending on OS
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Cumulative dot trail on transparent overlay (alpha layer not needed since we blend)
    dot_overlay = np.zeros((height, width, 3), dtype=np.uint8)

    # Assign unique colors for each ID
    id_colors = defaultdict(lambda: tuple(np.random.randint(0, 255, size=3).tolist()))

    # Run tracking
    results = model.track(source=input_path, stream=True, persist=True, conf=confidence, show=False)

    for result in results:
        frame = result.orig_img.copy()

        if result.boxes.id is not None:
            for box, track_id in zip(result.boxes.xyxy, result.boxes.id):
                x1, y1, x2, y2 = box.tolist()
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)
                tid = int(track_id.item())
                color = id_colors[tid]

                # Draw box and ID
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                cv2.putText(frame, f'ID {tid}', (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                # Draw persistent dot on dot_overlay
                cv2.circle(dot_overlay, (center_x, center_y), radius=3, color=color, thickness=-1)

        combined = cv2.addWeighted(frame, 1.0, dot_overlay, 1.0, 0)
        out.write(combined)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return output_path

def anam_detect(model,confidence : float, input_path: str, output_path: str):

    # Load video and model
    # Open video and get frame size & FPS
    cap = cv2.VideoCapture(input_path)
    ret, first_frame = cap.read()
    if not ret:
        raise RuntimeError("Failed to read video.")
    height, width = first_frame.shape[:2]
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Define output video writers
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    overlay_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Smoothing parameters
    alpha = 0.9
    smoothed_density = np.zeros((height, width), dtype=np.float32)
    smoothed_velocity = np.zeros((height, width), dtype=np.float32)

    # For tracking velocities
    prev_positions = {}

    # Tracking and processing loop
    for result in model.track(source=input_path, stream=True, persist=True, conf=confidence, classes=[0]):
        frame = result.orig_img.copy()
        density_map = np.zeros((height, width), dtype=np.float32)
        velocity_map = np.zeros((height, width), dtype=np.float32)

        new_positions = {}

        if result.boxes.id is not None:
            ids = result.boxes.id.cpu().numpy()
            boxes = result.boxes.xyxy.cpu().numpy()

            for tid, (x1, y1, x2, y2) in zip(ids, boxes):
                x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                x1 = max(0, min(width - 1, x1))
                y1 = max(0, min(height - 1, y1))
                x2 = max(0, min(width - 1, x2))
                y2 = max(0, min(height - 1, y2))

                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)
                new_positions[tid] = (cx, cy)

                # Compute area of the bounding box
                area = max(1, (x2 - x1) * (y2 - y1))  # avoid divide-by-zero
                norm_factor = 1.0 / area

                # Add normalized density
                density_map[y1:y2, x1:x2] += 1

                # Compute velocity and normalize if previous position exists
                if tid in prev_positions:
                    px, py = prev_positions[tid]
                    dx = cx - px
                    dy = cy - py
                    velocity = np.sqrt(dx ** 2 + dy ** 2)
                    velocity_map[y1:y2, x1:x2] += velocity * norm_factor  # normalize velocity as well

        prev_positions = new_positions

        # Temporal + spatial smoothing
        smoothed_density = alpha * smoothed_density + (1 - alpha) * density_map
        smoothed_velocity = alpha * smoothed_velocity + (1 - alpha) * velocity_map

        # Compute population flow
        population_flow = smoothed_density * (smoothed_velocity)
        

        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(population_flow, (0, 0), sigmaX=30, sigmaY=30)

        # Normalize and filter
        norm_flow = cv2.normalize(blurred, None, 0, 255, cv2.NORM_MINMAX)
        norm_flow[norm_flow < 25] = 0
        norm_flow = norm_flow.astype(np.uint8)

        # Generate heatmap
        color_map = cv2.applyColorMap(norm_flow, cv2.COLORMAP_JET)

        # Overlay on original frame
        dimmed_frame = (frame * 0.5).astype(np.uint8)
        overlay = cv2.addWeighted(dimmed_frame, 1.0, color_map, 0.6, 0)

        # Write output
        overlay_writer.write(overlay)

        # Display

    # Cleanup
    cap.release()
    overlay_writer.release()
    cv2.destroyAllWindows()
    return output_path

