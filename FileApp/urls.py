from django.urls import path
from .views import *

urlpatterns  = [
    path('createFile/', FilePostView.as_view(),name="createFile"),
    path('getFiles/', FilesView.as_view(),name="viewFiles"),
]