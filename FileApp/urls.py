from django.urls import path
from .views import *

urlpatterns  = [
    
    #vistas para peticiones REST
    path('createFile/', FilePostView.as_view(),name="createFile"),
    path('getFiles/', FilesView.as_view(),name="viewFiles"),
    path('updateFiles/', UpdateFile.as_view(), name="updateFile"),
    #vistas para peticiones SOAP
    
]