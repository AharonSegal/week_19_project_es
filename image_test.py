from PIL import Image, ExifTags
import pytesseract
from PIL.ExifTags import TAGS
import os

import hashlib


dir_path = "ingestion_service_api\images"
image_path = "tweet_0.png"

def image_process():
    img = Image.open(image_path)
    raw_text = pytesseract.image_to_string(img)
    print("---------img------------")
    print(img)
    print("---------raw_text------------")
    print(raw_text)

    print("---------meta------------")

    with Image.open(image_path) as img:
        metadata = {
            "filename": os.path.basename(image_path),
            "format": img.format,
            "width": img.size[0],
            "height": img.size[1],
            "mode": img.mode,             
            "file_size": os.path.getsize(image_path),
        }
    print(metadata)

    print("--------ID------------")

    sha = hashlib.sha256()
    with open(image_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha.update(chunk)
    res = sha.hexdigest()[:16]
    print(res)

print("Python Program to print list the files in a directory.")
Direc = dir_path
print(f"Files in the directory: {Direc}")
files = os.listdir(Direc)
# Filtering only the files.
files = [f for f in files if os.path.isfile(Direc+'/'+f)]
print(*files, sep="\n")