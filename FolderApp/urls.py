from django.urls import path, re_path
from .views import *

urlpatterns  = [
    path('createFolder/', RegisterFolder.as_view(),name="folder"),
    re_path(r'^getFolder/(?P<parentFolder>\d+)/$', GetFolderByParentId.as_view(),name="folderByParent"),
    path('getFolder/', GetFolderByParentId.as_view(),name="folderNotParent"),
    path('updateFolder/<int:folderId>/', UpdateFolder.as_view(), name="updateFolder")
]