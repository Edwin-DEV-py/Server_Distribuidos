from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from FileApp.models import FileModel, FilePaths
from FileApp.serializers import FileSerializer
from .serializers import *
from .models import *
from django.conf import settings
import jwt
import os
from django.db.models import Sum

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

#obtener las carpetas y archivos en una sola llamada
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
            
            #calcular el peso total de la carpeta actual
            total_storage = FolderModel.objects.filter(parentFolder=parentFolder, userId=user_id).aggregate(Sum('storage'))['storage__sum'] or 0
            
            #combinar los datos
            """
                DECIRLES A LSO CLIENTES QUE EL STORAGE DL FOLDER LLEGA EN BYTES
                POR LO TANTO ELLOS DEBEN CONVERTIR ESE VALOR EN MB O GB PARA
                MOSTRARLE AL USUARIO.
            """
            combined_data = []
            
            for folder_data in serializer_folder.data:
                folder_data['type'] = 'folder'
                combined_data.append(folder_data)
            
            for file_data in serializer_files.data:
                file_data['type'] = 'file'
                
                #obtener la extensiond el archivo
                file_name = file_data['fileName']
                file_extension = os.path.splitext(file_name)[1].lstrip('.')
                file_data['extension'] = file_extension
                
                #traer las rutas para pasarselas al cliente
                file_id = file_data['id']
                file_paths = FilePaths.objects.filter(file=file_id)
                file_data['paths'] = [file_path.filePath for file_path in file_paths]
                
                combined_data.append(file_data)
            
            return Response({'data': combined_data, 'TotalStorage': total_storage})
        except jwt.exceptions.InvalidTokenError:
            return Response({'error': 'Token inválido'}, status=status.HTTP_401_UNAUTHORIZED)

#editar y eliminar una carpeta
class UpdateFolder(APIView):
    
    def get(self,request, folderId):
        folder = FolderModel.objects.get(id=folderId)
        serializer = FolderSerializer(folder)
        return Response(serializer.data)
    
    def post(self,request, folderId):
        
        #verificar el token
        token = request.headers.get('Authorization', '').split(' ')[1]
        
        try:
            user = jwt.decode(token, settings.SECRET_TOKEN_KEY, algorithms=['HS256'])
            user_id = user['user_id']
            
            folder = FolderModel.objects.get(id=folderId, userId=user_id)
            print(folder)
            folder.folderName = request.data.get('folderName')
            parent_folder_id = request.data.get('parentFolder')
            if parent_folder_id is not None:
                folder.parentFolder = parent_folder_id
            folder.storage = request.data.get('storage')
            
            folder.save()
            serializers = FolderSerializer(folder)
            return Response(serializers.data)
        except jwt.exceptions.InvalidTokenError:
            return Response({'error': 'Token inválido'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, folderId):
        
        #verificar el token
        token = request.headers.get('Authorization', '').split(' ')[1]
        
        try:
            user = jwt.decode(token, settings.SECRET_TOKEN_KEY, algorithms=['HS256'])
            user_id = user['user_id']
            
            files_in_folder = FileModel.objects.filter(folderParent=folderId,userId=user_id).delete()
            folders_in_folder = FolderModel.objects.filter(parentFolder=folderId, userId=user_id)
            for folder_in_folder in folders_in_folder:
                self.delete_subfolder(folder_in_folder.id)
            
            folder = FolderModel.objects.get(id=folderId, userId=user_id)
            folder.delete()
            
            return Response({'message:': 'carpeta eliminada'})
            
        except jwt.exceptions.InvalidTokenError:
            return Response({'error': 'Token inválido'}, status=status.HTTP_401_UNAUTHORIZED)

    #funsion recursiva para borrar archivos de subfolders
    def delete_subfolder(self, folderId):
        #Recursivamente eliminar subcarpetas y archivos
        files_in_folder = FileModel.objects.filter(folderParent=folderId).delete()
        folders_in_folder = FolderModel.objects.filter(parentFolder=folderId)
        for folder_in_folder in folders_in_folder:
            self.delete_subfolder(folder_in_folder.id)
        folder = FolderModel.objects.get(id=folderId)
        folder.delete()