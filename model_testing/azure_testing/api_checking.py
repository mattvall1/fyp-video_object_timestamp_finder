# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Dev file for checking FastAPIs
import requests

def upload_image(file_path):
    url = "http://127.0.0.1:8000/upload-image/"
    files = {"file": open(file_path, "rb")}
    response = requests.post(url, files=files)

    print(response.json())

def delete_image(file_name):
    url = f"http://127.0.0.1:8000/delete-image/{file_name}"
    response = requests.delete(url)

    print(response.json())

upload_image("../../testing_images/cat_1.jpeg")

# delete_image("cat_1.jpeg")
