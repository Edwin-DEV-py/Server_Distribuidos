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
from django.http import HttpResponse, HttpRequest
from django.db.models import Sum
from spyne.error import ResourceNotFoundError
from .serializers import *
import os
from .models import *
from collections import OrderedDict
import base64

class SoapServiceUser(ServiceBase):
    
    @rpc(Unicode, Unicode, _returns=Unicode)
    def loginSoap(ctx, username, password):
        
        response_data = loginSoapView(username, password)
        
        if 'token' in response_data:
            return response_data['token']
        elif 'error_message' in response_data:
            return response_data['error_message']
        else:
            return 'Error desconocido'
        
    @rpc(Unicode, Unicode, Unicode, Unicode, Unicode, _returns=Unicode)
    def resgisterSoap(ctx, username, name, email, age, password):
        
        response = registerSoapView(username,name,email,age,password)
        
        if 'message' in response:
            return response['message']
        elif 'error_message' in response:
            return response['error_message']
        else:
            return 'Error desconocido'
    
my_soap = Application(
    [SoapServiceUser],
    tns='django.soap.users',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11(),
)

def my_soap_consulta_users():
    
    django_app = DjangoApplication(my_soap)
    my_soap_app = csrf_exempt(django_app)
    
    return my_soap_app
