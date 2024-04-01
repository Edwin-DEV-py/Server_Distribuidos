from django.urls import path
from .views import *

urlpatterns  = [
    
    #vistas para peticiones REST
    path('createFile/', FilePostView.as_view(),name="createFile"),
    path('getFiles/', FilesView.as_view(),name="viewFiles"),
    
    #vistas para peticiones SOAP
    
]