from django.urls import path
from .views import *

urlpatterns  = [
    
    #vistas para peticiones REST
    path('createFile/', FilePostView.as_view(),name="createFile"),
    path('getFiles/', FilesView.as_view(),name="viewFiles"),
    path('updateFiles/', UpdateFile.as_view(), name="updateFile"),
    path('sendFiles/', FilePostViewByUserId.as_view(),name="sendFiles"),
    #prueba
    path('download/<path:path>/', DownloadFileView.as_view(), name='descargar_archivo'),
    #vistas para peticiones SOAP
    
]