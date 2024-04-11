import base64
from zeep import Client
import os


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_image

def get_filename(image_path):
    return os.path.basename(image_path)

def get_filesize(image_path):
    return os.path.getsize(image_path)


image_paths = ["C:/Users/nicol/Downloads/create-a-32x32-pixel-art.png", "C:/Users/nicol/Downloads/create-a-32x32-pixel-art.png"]
tokem = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEyOTk2NzM4LCJpYXQiOjE3MTE3MDA3MzgsImp0aSI6Ijc2NzVmYzcyN2Q3OTRlYWNiNzk4MDVmODkxZmNhNjdlIiwidXNlcl9pZCI6ImFkbWluIn0.oAJvSszHmqzOwdkltgUIOEfVlr1w1gTPwdDLBpyn7M4'

files_info = []

for image_path in image_paths:
    filename = get_filename(image_path)
    filesize = get_filesize(image_path)
    encoded_image = encode_image(image_path)
    files_info.append({"filename": filename, "filesize": filesize, "encoded_image": encoded_image})


client = Client('http://127.0.0.1:8000/files/soap/?wsdl')

for file_info in files_info:
    response = client.service.process_file(tokem, file_info["filename"], file_info["filesize"], file_info["encoded_image"], 0)
    print(response)