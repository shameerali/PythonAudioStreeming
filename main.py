# from http.client import HTTPException
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
import os
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# Set up templates directory
templates = Jinja2Templates(directory="templates")

# Mount static directory
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# @app.get("/")
# def read_root():
#     return {"message": "Server is running!"}



@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/uploadFile", response_class=HTMLResponse)
async def read_upload_files(request: Request):
    return templates.TemplateResponse("upload_file.html", {"request": request})

@app.get("/savedFiles", response_class=HTMLResponse)
async def read_saved_files(request: Request):

    datass = getAllAudioFilesTwo()
    print("datatta")
    print(datass)
    print(datass.get("files"))
    context = {"request": request, "items": datass.get("files")}
    return templates.TemplateResponse("saved_files.html", context)


# @app.get("/", response_class=HTMLResponse)
# async def root(request: Request):
#         context = {"request": request, "items": ["Item 1", "Item 2", "Item 3"]}
#         return templates.TemplateResponse("index.html", context)



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


def getAllAudioFilesTwo(directory: str = None):
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