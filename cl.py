import base64
from zeep import Client
import os
import hashlib


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_image

def get_filename(image_path):
    return os.path.basename(image_path)

def get_filesize(image_path):
    return os.path.getsize(image_path)

def calculate_sha256(file_path):
    with open(file_path, "rb") as file:
        file_content = file.read()
        sha256_hash = hashlib.sha256(file_content).hexdigest()
    return sha256_hash

image_paths = ["C:/Users/nicol/Downloads/file.png"]
tokem = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE0MzQ0NjY1LCJpYXQiOjE3MTMwNDg2NjUsImp0aSI6ImVkYjkzMTkwOGI5YjQ2MGJhZDU2MWIzNDcxNDc1YTNmIiwidXNlcl9pZCI6ImFkbWluIn0.PIe92t-GAtNrMB6q8dYOtMUSqWLTQXCy9wlV_M3Zd6Y'
files_info = []

for image_path in image_paths:
    filename = get_filename(image_path)
    filesize = get_filesize(image_path)
    encoded_image = encode_image(image_path)
    file_sha256 = calculate_sha256(image_path)
    files_info.append({"filename": filename, "filesize": filesize, "encoded_image": encoded_image, "file_hash": file_sha256})


client = Client('http://172.171.240.20:8000/files/soap/?wsdl')

for file_info in files_info:
    response = client.service.process_file(tokem, file_info["filename"], file_info["filesize"], file_info["encoded_image"], file_info["file_hash"], 0)
    print(response)