# from http.client import HTTPException
from fastapi import FastAPI, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import os
from fastapi.staticfiles import StaticFiles


app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def read_root():
    return {"message": "Server is running!"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()  # This reads the file content into memory
    filename = file.filename
    content_type = file.content_type

    # You can save it to disk if needed
    with open(f"uploads/uploaded_{filename}", "wb") as f:
        f.write(contents)

    return {"filename": filename, "content_type": content_type}

@app.get("/getAllAudioFiles")
async def getAllAudioFiles(directory: str = None):
    # Set default directory if none provided
    if directory is None:
        directory = "uploads"  # Your default directory

    # Verify directory exists
    if not os.path.isdir(directory):
        return JSONResponse(
            status_code=404,
            content={"message": f"Directory '{directory}' not found"}
        )

    # List all files (excluding subdirectories)
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    return {"directory": directory, "files": files}