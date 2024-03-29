from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns  = [
    path('login/', AuthenticationView.as_view(), name="login"),
    path('user/', VerifyUserView.as_view(), name="user"),
    path('login2/', TokenObtainPairView.as_view(), name="login2")
]