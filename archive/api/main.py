# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: FastAPI for running image recognition and object detection via Azure Web App
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os


# Setup FastAPI and create the images directory
app = FastAPI()
upload_dir = "images"
os.makedirs(upload_dir, exist_ok=True)


@app.get("/")
def read_root():
    return {"tryAzure": ""}


# Mount the uploaded_images directory
app.mount("/images", StaticFiles(directory=upload_dir), name="images")


@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    with open(f"{upload_dir}/{file.filename}", "wb") as buffer:
        buffer.write(file.file.read())

    return {"filename": file.filename}


@app.get("/images/")
async def list_uploaded_images():
    uploaded_images = os.listdir(upload_dir)
    return JSONResponse(content={"uploaded_images": uploaded_images})


@app.delete("/delete-image/{file_name}")
async def delete_image(file_name: str):
    file_path = f"{upload_dir}/{file_name}"
    if os.path.exists(file_path):
        os.remove(file_path)
        return JSONResponse(
            content={"message": "File deleted successfully"}, status_code=200
        )
    else:
        return JSONResponse(content={"message": "File not found"}, status_code=404)
