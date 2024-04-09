from django.views.decorators.csrf import csrf_exempt
from spyne.application import Application
from spyne.decorator import rpc
from spyne.model.primitive import Unicode, Integer, Double, String, DateTime, Date
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from spyne.service import ServiceBase
import json
from spyne import Iterable, Array
from spyne import ComplexModel
from django.forms.models import model_to_dict
from django.db import IntegrityError
from spyne.error import ResourceNotFoundError
from spyne.model.fault import Fault
from django.db.models.deletion import ProtectedError
from .views import *
from django.http import HttpResponse
from django.db.models import Sum
from spyne.error import ResourceNotFoundError
from .serializers import *
import os
from .models import *
from collections import OrderedDict

class FolderSoapModel(ComplexModel):
    __namespace__ = "folders"
    id = Integer
    folderName = String
    storage = Integer
    userId = String
    parentFolder = Integer
    createdAt = DateTime
    
class FileSoapModel(ComplexModel):
    __namespace__ = "files"
    id = Integer
    fileName = String
    folderParent = Integer
    userId = String
    createdAt = DateTime

class FileAndFolderModel(ComplexModel):
    __namespace__ = "filesAndFolders"
    id = Integer
    folderName = String
    fileName = String
    storage = Integer
    userId = String
    parentFolder = Integer
    createdAt = DateTime
    type = String
    paths = Array(String)
    extension = String

class SoapService(ServiceBase):
    
    @rpc(_returns=Array(FolderSoapModel))
    def list(ctx):
        folders = FolderModel.objects.values('id','folderName','storage','userId','parentFolder')
        return folders
    
    @rpc(Unicode, Unicode, _returns=Array(FileAndFolderModel), _out_variable_name='files')
    def get_folders_by_parent_id(ctx, token, parentFolder):
        try:
            # Obtener el token
            user = jwt.decode(token, settings.SECRET_TOKEN_KEY, algorithms=['HS256'])
            user_id = user['user_id']

            # Obtener archivos y carpetas
            folders_data = FolderModel.objects.filter(parentFolder=parentFolder, userId=user_id).values('id', 'folderName', 'storage', 'userId', 'parentFolder')
            files_data = FileModel.objects.filter(folderParent=parentFolder, userId=user_id).values('id', 'fileName', 'folderParent', 'userId')

            # Convertir los QuerySets a listas
            folders = [FolderSoapModel(**folder) for folder in folders_data]
            files = [FileSoapModel(**file) for file in files_data]
            
            for folder in folders:
                folder.type = 'folder'
            for file in files:
                file.type = 'file'
                
            #obtener los paths
            file_paths = FilePaths.objects.filter(file__in=[file.id for file in files])
            file_paths_data = {}
            for file_path in file_paths:
                file_paths_data.setdefault(file_path.file_id, []).append(file_path.filePath)
            
            for file in files:
                file.paths = file_paths_data.get(file.id, [])
                
                #obtener la extension dle archivo
                file_name = file.fileName
                file_extension = os.path.splitext(file_name)[1].lstrip('.')
                file.extension = file_extension

            all_items = folders + files
            
            return all_items
        except jwt.exceptions.InvalidTokenError:
            return "Token inválido"

    
my_soap = Application(
    [SoapService],
    tns='django.soap.example',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11(),
)

def my_soap_consulta():
    
    django_app = DjangoApplication(my_soap)
    my_soap_app = csrf_exempt(django_app)
    
    return my_soap_app