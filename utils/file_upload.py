import os
from uuid import uuid4
from fastapi import UploadFile

UPLOAD_DIR = "uploads"

def save_file(file: UploadFile, folder: str) -> str:
    
    path = os.path.join(UPLOAD_DIR, folder)
    os.makedirs(path, exist_ok=True)
    ext = file.filename.split(".")[-1]
    filename = f"{uuid4()}.{ext}"

    file_path = os.path.join(path, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return file_path