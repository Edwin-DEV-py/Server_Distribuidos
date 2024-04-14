from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView
from .view_soap import *

urlpatterns  = [
    path('login/', AuthenticationView.as_view(), name="login"),
    path('user/', VerifyUserView.as_view(), name="user"),
    path('login2/', TokenObtainPairView.as_view(), name="login2"),

    #vistas soap
    path('soap/', my_soap_consulta_users())
]