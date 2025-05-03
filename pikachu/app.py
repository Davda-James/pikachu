from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import Response
from contextlib import asynccontextmanager
from ultralytics import YOLO
from pikachu.model.object_detection import detect_objects_in_video as detect_objects
import uuid
import shutil
import os
import yaml

@asynccontextmanager
async def lifespan(app: FastAPI):
    # load the config file
    with open("config.yaml") as f:
        config=yaml.safe_load(f)
    app.state.config = config

    # Load the model weights
    model = YOLO(config["weights"]["path"])

    app.state.model = model
    yield


app = FastAPI(lifespan=lifespan)

# object_detection
# object_tracking
# 



@app.head("/")
def server_check():
    return Response(status_code=200)   

@app.get("/")
def server_status():
    return {"status":"running"}

@app.get("/detect")
async def detect(request: Request, file: UploadFile = File(...)):
    os.makedirs("temp", exist_ok=True)
    input_path = f"temp/{uuid.uuid4()}.mp4"
    output_path = f"temp/output_{uuid.uuid4()}.mp4"

    # Save uploaded video
    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Run detection
    detect_objects(request.app.state.model, input_path, output_path)

    # Return processed video
    return FileResponse(output_path, media_type="video/mp4", filename="processed.mp4")
        

