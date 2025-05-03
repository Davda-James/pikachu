from fastapi import FastAPI, Request, UploadFile, File , HTTPException
from fastapi.responses import Response,FileResponse
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

@app.post("/detect")
async def detect(request: Request, file: UploadFile = File(...)):
    
    TEMP_DIR_PATH = request.app.state.config["temp_files"]["path"]
    INPUT_DIR = os.path.join(TEMP_DIR_PATH, "input")
    OUTPUT_DIR = os.path.join(TEMP_DIR_PATH, "output")

    os.makedirs(TEMP_DIR_PATH, exist_ok=True)
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    file_uuid = uuid.uuid4()
    input_path = os.path.join(INPUT_DIR, f"{file_uuid}.mp4")
    output_path = os.path.join(OUTPUT_DIR, f"{file_uuid}.mp4")
    try:
        # Save uploaded video
        with open(input_path, "wb") as f:
            content = file.file.read()
            f.write(content)

        if not os.path.exists(input_path):
            raise HTTPException(status_code=500, detail=f"Failed to save input file at {input_path}")
        
        if os.path.getsize(input_path) == 0:
            os.remove(input_path)
            raise HTTPException(status_code=400, detail="Uploaded file is empty")

        # Run detection
        output_video= detect_objects(request.app.state.model, input_path,output_path, TEMP_DIR_PATH,INPUT_DIR,OUTPUT_DIR)
        
        # Return processed video
        response = FileResponse(output_video, media_type="video/mp4", filename="processed.mp4")

        # if os.path.exists(output_video):
        #     os.remove(output_video)

        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = f"temp/output/track/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="video/x-msvideo", filename=filename)
