from django.urls import path
from .views import *

urlpatterns  = [
    path('createFolder/', RegisterFolder.as_view(),name="folder"),
    path('getFolder/<int:parentFolder>/', GetFolderByParentId.as_view(),name="folderByParent"),
]