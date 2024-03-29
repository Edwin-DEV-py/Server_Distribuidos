from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from FileApp.models import FileModel
from FileApp.serializers import FileSerializer
from .serializers import *
from .models import *
from django.conf import settings
import jwt

class RegisterFolder(APIView):

    def get(self,request):
        #verificar el token
        token = request.headers.get('Authorization', '').split(' ')[1]
        
        try:
            #decodificar el token
            user = jwt.decode(token, settings.SECRET_TOKEN_KEY, algorithms=['HS256'])
            
            folders = FolderModel.objects.all()
            serializer = FolderSerializer(folders,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except jwt.exceptions.InvalidTokenError:
            return Response({'error': 'Token inválido'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def post(self,request):

        #verificar el token
        token = request.headers.get('Authorization', '').split(' ')[1]
        
        try:
            #decodificar el token
            user = jwt.decode(token, settings.SECRET_TOKEN_KEY, algorithms=['HS256'])
            user_id = user['user_id']
            
            request.data['userId'] = user_id
            
            serializer = FolderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.InvalidTokenError:
            return Response({'error': 'Token inválido'}, status=status.HTTP_401_UNAUTHORIZED)

class GetFolderByParentId(APIView):

    def get(self,request,parentFolder=0):
        
        #verificar el token
        token = request.headers.get('Authorization', '').split(' ')[1]
        
        try:
            #decodificar el token
            user = jwt.decode(token, settings.SECRET_TOKEN_KEY, algorithms=['HS256'])
            user_id = user['user_id']
            
            #obtener las carpetas
            folder = FolderModel.objects.filter(parentFolder=parentFolder, userId=user_id)
            serializer_folder = FolderSerializer(folder, many=True)
            
            #obtener los archivos
            files = FileModel.objects.filter(folderParent=parentFolder, userId=user_id)
            serializer_files = FileSerializer(files, many=True)
            
            #combinar los datos
            combined_data = []
            
            for folder_data in serializer_folder.data:
                folder_data['type'] = 'folder'
                combined_data.append(folder_data)
            
            for file_data in serializer_files.data:
                file_data['type'] = 'file'
                combined_data.append(file_data)
            
            return Response(combined_data)
        except jwt.exceptions.InvalidTokenError:
            return Response({'error': 'Token inválido'}, status=status.HTTP_401_UNAUTHORIZED)

class UpdateFolder(APIView):
    
    def get(self,request, folderId):
        folder = FolderModel.objects.get(id=folderId)
        serializer = FolderSerializer(folder)
        return Response(serializer.data)
    
    def post(self,request, folderId):
        
        folder = FolderModel.objects.get(id=folderId)
        
        folder.folderName = request.data.get('folderName')
        folder.parentFolder = request.data.get('parentFolder')
        folder.storage = request.data.get('storage')
        
        folder.save()
        serializers = FolderSerializer(folder)
        return Response(serializers.data)
        