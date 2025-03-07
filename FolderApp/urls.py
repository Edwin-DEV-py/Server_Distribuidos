from django.urls import path, re_path
from .views import *
from .views_soap import *

urlpatterns  = [
    #vista para peticiones REST
    path('createFolder/', RegisterFolder.as_view(),name="folder"),
    re_path(r'^getFolder/(?P<parentFolder>\d+)/$', GetFolderByParentId.as_view(),name="folderByParent"),
    path('getFolder/', GetFolderByParentId.as_view(),name="folderNotParent"),
    path('updateFolder/<int:folderId>/', UpdateFolder.as_view(), name="updateFolder"),
    path('shareFolder/<int:folderId>/', ShareFolder.as_view(), name='shareFolder'),
    #vista para peticiones SOAP
    path('soap/', my_soap_consulta())
]