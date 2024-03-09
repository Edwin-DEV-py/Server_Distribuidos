from django.urls import path
from .views import *

urlpatterns  = [
    path('login/', AuthenticationView.as_view(), name="login")
]