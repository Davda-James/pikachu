from ultralytics import YOLO
import cv2
from fastapi import Request

def detect_objects_in_video(model,input_path: str, output_path: str):
    # Load YOLO model
    # model = YOLO("../hackathon/yolov8/runs/detect/train9/weights/best.pt")
    # model = request.app.state.model

    # Video paths
    # video_path = "videos/06.mp4"
    # output_path = "output_new_best.mp4"

    # Open video
    cap = cv2.VideoCapture(input_path)
    assert cap.isOpened(), f"Cannot open video {input_path}"

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Run object tracking
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Run tracking
        results = model.track(source=frame, persist=True, stream=False, verbose=False)

        # Extract results
        if results and results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()         # [x1, y1, x2, y2]
            ids = results[0].boxes.id.cpu().numpy().astype(int) # Track IDs

            for box, obj_id in zip(boxes, ids):
                x1, y1, x2, y2 = map(int, box)
                label = f"id{obj_id}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=1)
                cv2.putText(frame, label, (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # Write frame
        out.write(frame)

    # Cleanup
    cap.release()
    out.release()
    
