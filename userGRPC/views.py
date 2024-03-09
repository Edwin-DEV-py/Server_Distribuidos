from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from grpc import insecure_channel


class AuthenticationView(APIView):
    
    def post(self, request):
        serializers = UserCredentialsSerializer(data=request.data)
        
        if serializers.is_valid():
            
            username = serializers.validated_data.get('username')
            password = serializers.validated_data.get('password')