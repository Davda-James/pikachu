from fastapi import FastAPI, Request, UploadFile, File , HTTPException
from fastapi.responses import Response,FileResponse,StreamingResponse
from contextlib import asynccontextmanager
from ultralytics import YOLO
from pikachu.model.object_detection import detect_objects_in_video as detect_objects, track_flow
import uuid
import os
import yaml

@asynccontextmanager
async def lifespan(app: FastAPI):
    # load the config file
    with open("config.yaml") as f:
        config=yaml.safe_load(f)

    # Define the paths once
    app.state.config = config
    temp_dir = config["temp_files"]["path"]
    app.state.input_dir = os.path.join(temp_dir, "input")
    app.state.output_dir = os.path.join(temp_dir, "output")
    app.state.track_dir = os.path.join(app.state.output_dir, "track")

    os.makedirs(app.state.input_dir, exist_ok=True)
    os.makedirs(app.state.output_dir, exist_ok=True)
    os.makedirs(app.state.track_dir, exist_ok=True)

    # Load the model weights
    model = YOLO(config["weights"]["path"])

    app.state.model = model
    yield


app = FastAPI(lifespan=lifespan)


@app.head("/")
def server_check():
    return Response(status_code=200)   

@app.get("/")
def server_status():
    return {"status":"running"}


@app.post("/detect")
async def detect(request: Request, file: UploadFile = File(...),
                confidence: float = 0.5):
    
    # TEMP_DIR_PATH = request.app.state.config["temp_files"]["path"]
    INPUT_DIR = app.state.input_dir
    OUTPUT_DIR = app.state.output_dir

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
        output_video= detect_objects(request.app.state.model, confidence, input_path,output_path)
        
        
        # Stream video and clean up after response
        def stream_and_cleanup():
            with open(output_video, "rb") as video:
                yield from video
            # Cleanup after streaming
            os.remove(output_path)
        
        # Return processed video
        return  StreamingResponse(stream_and_cleanup(), media_type="video/mp4", headers={"Content-Disposition": "attachment; filename=processed.mp4"})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

@app.post("/track")
def track_path(request: Request, file: UploadFile = File(...),
               confidence : float = 0.5):
    INPUT_DIR = request.app.state.input_dir
    OUTPUT_DIR = request.app.state.output_dir

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
        
        # Call the track_path function
        output_video = track_flow(request.app.state.model, confidence, input_path, output_path)
        # Stream video and clean up after response
        def stream_and_cleanup():
            with open(output_video, "rb") as video:
                yield from video

            os.remove(output_path)
        
        return StreamingResponse(stream_and_cleanup(), media_type="video/mp4", headers={"Content-Disposition": "attachment; filename=processed.mp4"})
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    