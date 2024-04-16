from rest_framework.views import APIView
from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from FileApp.forms import FileUploadForm
from .serializers import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
import requests
from rest_framework.renderers import TemplateHTMLRenderer
from django.conf import settings
import os
import jwt
from django.db import transaction
from FolderApp.models import FolderModel
from django.db.models import F
from django.http import HttpResponse
import mimetypes
from rest_framework.decorators import parser_classes
import base64
import re
import grpc
import upload_pb2 as grpc_pb2
import upload_pb2_grpc as grpc_pb2_grpc

#funcion para guardar archivos
class FilePostView(APIView):
    
    parser_classes = (MultiPartParser, FormParser)
    
    def get(self, request):
        form = FileUploadForm()
        return render(request, 'form1.html', {'form': form, 'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEyOTk2NzM4LCJpYXQiOjE3MTE3MDA3MzgsImp0aSI6Ijc2NzVmYzcyN2Q3OTRlYWNiNzk4MDVmODkxZmNhNjdlIiwidXNlcl9pZCI6ImFkbWluIn0.oAJvSszHmqzOwdkltgUIOEfVlr1w1gTPwdDLBpyn7M4'})
    
    def post(self,request, *args, **kwargs):
        
        #verificar el token
        #token = request.headers.get('Authorization', '').split(' ')[1]
        token = request.POST.get('token')
        
        try:
            user = jwt.decode(token, settings.SECRET_TOKEN_KEY, algorithms=['HS256'])
            user_id = user['user_id']
            
            folder_id = request.data.get('folderParent')
            if folder_id is None:
                folder_id = 0
            
            files = request.FILES.getlist('files')
            file_send_list = []
            
            print(files)
            for file in files:
                file_name = file.name
                file_size = file.size
                print(file_size)
                data = {
                    'userId': user_id,
                    'fileName': file_name,
                    'folderParent': folder_id
                }
                serializers = FileSerializer(data=data)
                
                if serializers.is_valid():
                    
                    #transaccion atomica para evitar perdida de datos
                    with transaction.atomic():
                        instance = serializers.save()
                        file_send_list.append(data)
                        
                        #datos que seran enviados al servidor
                        data_send_server = {
                            'userId': user_id,
                            'file': file,
                            'file_id': instance.id
                        }
                        
                        #actualizar el espacio del folder
                        if folder_id != 0:
                            update_storage_folder = FolderModel.objects.get(id=folder_id)
                            update_storage_folder.storage = F('storage') + file_size
                            update_storage_folder.save()
                        
                        response = Send_data_to_FileServer(data_send_server)
                        if not response:
                            raise Exception("Ocurrio un error con el servidor de archivos")
                else:
                    return Response(serializers.errors)
                
            return Response(file_send_list, status=status.HTTP_201_CREATED)
        except jwt.exceptions.InvalidTokenError:
            return Response({'error': 'Token inválido'}, status=status.HTTP_401_UNAUTHORIZED)
        
#Funcion para guardar archivos con el id del usuario
@parser_classes((MultiPartParser, FormParser))
def file_post_view_by_user_id(token, fileName, fileSize, file, folder_id=0):
    
    user = jwt.decode(token, settings.SECRET_TOKEN_KEY, algorithms=['HS256'])
    user_id = user['user_id']

    if folder_id is None:
            folder_id = 0
    print(file)
    data = {
        'userId': user_id,
        'fileName': fileName,
        'folderParent': 0
    }
    serializers = FileSerializer(data=data)
    if serializers.is_valid():
        
        #transacción atómica para evitar pérdida de datos
        with transaction.atomic():
            instance = serializers.save()
            
            #datos que serán enviados al servidor
            data_send_server = {
                'userId': user_id,
                'file': file,
                'file_id': instance.id
            }
            
            #actualizar el espacio del folder
            if folder_id != 0:
                update_storage_folder = FolderModel.objects.get(id=folder_id)
                update_storage_folder.storage = F('storage') + fileSize
                update_storage_folder.save()
            
            response = Send_data_to_FileServer(data_send_server)
            if not response:
                raise Exception("Ocurrió un error con el servidor de archivos")
    else:
        return Response(serializers.errors)
    
    return Response(data, status=status.HTTP_201_CREATED)

#funcion para enviar los archivos al servidor
def Send_data_to_FileServer(data):
    
    try:
        
        channel = grpc.insecure_channel('172.171.240.20:5000')
        stub = grpc_pb2_grpc.FileServiceStub(channel)
        
        fileData = grpc_pb2.FileUploadRequest(
            file_id= data.get('file_id'),
            owner_id= data.get('userId'),
            binary_file= data.get('file')
        )
        
        sendData = stub.Upload(fileData)
        
        if sendData:
            print(sendData)
            #return Response(sendData)
        
        example_response = {
            'file_id': data.get('file_id'),
            'urls': [
                'ruta1/',
                'ruta2/'
            ]
        }
        
        urls = example_response.get('urls')
        
        file_instance = FileModel.objects.get(id=example_response.get('file_id'))
        for url in urls:
            file_path = FilePaths(file=file_instance, filePath=url)
            file_path.save()
            
        return True
    except Exception as e:
        print("Error al enviar los datos:", e)
        return False

        
class FilesView(APIView):
    
    def get(self,request):
        
        files = FileModel.objects.all()
        serializers = FileSerializer(files, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
#editar archivo
class UpdateFile(APIView):
    
    def post(self, request):
        
        #verificar el token
        token = request.headers.get('Authorization', '').split(' ')[1]
        
        try:
            user = jwt.decode(token, settings.SECRET_TOKEN_KEY, algorithms=['HS256'])
            user_id = user['user_id']
            file_id = request.data.get('fileId')
            file = FileModel.objects.get(userId=user_id, id=file_id)
            
            parent_folder_id = request.data.get('folderParent')
            if parent_folder_id is not None:
                file.folderParent = parent_folder_id
            file.fileName = request.data.get('filename')
            
            file.save()
            serializers = FileSerializer(file)
            return Response(serializers.data)
            
        except jwt.exceptions.InvalidTokenError:
            return Response({'error': 'Token inválido'}, status=status.HTTP_401_UNAUTHORIZED)
        
    def delete(self, request):
        #verificar el token
        token = request.headers.get('Authorization', '').split(' ')[1]

        try:
            user = jwt.decode(token, settings.SECRET_TOKEN_KEY, algorithms=['HS256'])
            user_id = user['user_id']

            #obtener los IDs
            file_ids = request.data.get('fileIds')

            #verificar si se proporciono una lista
            if isinstance(file_ids, list):
                for file_id in file_ids:
                    try:
                        file = FileModel.objects.get(userId=user_id, id=file_id)
                        file.delete()
                    except FileModel.DoesNotExist:
                        pass
            else:
                file_id = file_ids
                try:
                    file = FileModel.objects.get(userId=user_id, id=file_id)
                    file.delete()
                except FileModel.DoesNotExist:
                    pass

            return Response({'message': 'Archivos eliminados correctamente'})

        except jwt.exceptions.InvalidTokenError:
            return Response({'error': 'Token inválido'}, status=status.HTTP_401_UNAUTHORIZED)

#editar archivo con soap
def updateFile(token, fileId, fileName, folderParent):
        
    #verificar el token
    user = jwt.decode(token, settings.SECRET_TOKEN_KEY, algorithms=['HS256'])
    user_id = user['user_id']
    
    try:
        user = jwt.decode(token, settings.SECRET_TOKEN_KEY, algorithms=['HS256'])
        user_id = user['user_id']
        file = FileModel.objects.get(userId=user_id, id=fileId)
        
        if folderParent is not None:
            file.folderParent = folderParent
        file.fileName = fileName
        
        file.save()
        serializers = FileSerializer(file)
        return Response(serializers.data)
        
    except jwt.exceptions.InvalidTokenError:
        return "Token inválido"

#eliminar archivo con soap
def deleteFile(token, filesId):
        
    #verificar el token
    user = jwt.decode(token, settings.SECRET_TOKEN_KEY, algorithms=['HS256'])
    user_id = user['user_id']
    
    try:
        user = jwt.decode(token, settings.SECRET_TOKEN_KEY, algorithms=['HS256'])
        user_id = user['user_id']
        
        if isinstance(filesId, list):
            for file_id in filesId:
                try:
                    file = FileModel.objects.get(userId=user_id, id=file_id)
                    file.delete()
                except FileModel.DoesNotExist:
                    pass
        else:
            file_id[0] = filesId
            try:
                file = FileModel.objects.get(userId=user_id, id=file_id)
                file.delete()
            except FileModel.DoesNotExist:
                pass
        
    except jwt.exceptions.InvalidTokenError:
        return "Token inválido"


class DownloadFileView(APIView):
    
    def get(self, request, path):
        
        #para probar
        pathFile = os.path.join(settings.MEDIA_ROOT, path)
        
        if os.path.exists(pathFile):
            
            content_type, _ = mimetypes.guess_type(pathFile)
            if content_type is None:
                content_type = 'application/octet-stream'
                
            #abrir y leer el archivo
            with open(pathFile, 'rb') as download:
                
                response = HttpResponse(download.read(), content_type=content_type)
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(pathFile)}"'
                return response
        else:
            return HttpResponse("El archivo solicitado no existe", status=404)
        
        
#Descargar archivo desde el servidor donde esta almacenado
class DownloadFileAPIView(APIView):
    def post(self, request):
        path = request.data.get('pathFile', None)

        if path is None:
            return Response("Debe proporcionar la URL", status=status.HTTP_400_BAD_REQUEST)

        try:
            #Solicitud al servidor de archivos
            response = requests.get(path)
            response.raise_for_status()
            file = response.content

            #Extraee el nombre del archivo
            fileName = path.split('/')[-1]

            response = Response(file, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{fileName}"'
            return response
        
        except requests.exceptions.RequestException as e:
            return Response(f"No se pudo descargar el archivo: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

#Compartir un archivo a otro usuario
