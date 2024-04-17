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
import base64


class SoapServiceFiles(ServiceBase):
    
    @rpc(Unicode, Unicode, Unicode, Unicode, Unicode, _returns=Unicode)
    def process_file(ctx, token, fileName, fileSize, file, folderParent):
        try:
            response = file_post_view_by_user_id(token, fileName, fileSize, file)
            if response.status_code == 201:
                return 'Creado correctamente'
            else:
                return 'no se guardaron los archivos'
        except jwt.exceptions.InvalidTokenError:
            return "Token inválido"
        except Exception as e:
            return f"Ocurrió un error al procesar el archivo: {str(e)}"
        
    @rpc(Unicode, Unicode, Unicode, Unicode, _returns=Unicode)
    def update_file(ctx, token, fileId ,fileName, folderParent):
        try:

            response = updateFile(token, fileId,fileName, folderParent)
            if response.status_code == 203:
                return 'actualizado correctamente'
            else:
                return 'no se actualizo el archivo'
        except jwt.exceptions.InvalidTokenError:
            return "Token inválido"
        except Exception as e:
            return f"Ocurrió un error al procesar el archivo: {str(e)}"
        
    @rpc(Unicode, Unicode, _returns=Unicode)
    def delete_file(ctx, token, fileId):
        try:

            response = deleteFile(token, fileId)
            if response.status_code == 200:
                return 'eliminado correctamente'
            else:
                return 'no se elimino el archivo'
        except jwt.exceptions.InvalidTokenError:
            return "Token inválido"
        except Exception as e:
            return f"Ocurrió un error al procesar el archivo: {str(e)}"
        
my_soap = Application(
    [SoapServiceFiles],
    tns='django.soap.files',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11(),
)

def my_soap_consulta_files():
    
    django_app = DjangoApplication(my_soap)
    my_soap_app = csrf_exempt(django_app)
    
    return my_soap_app
