from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from grpc import insecure_channel
import requests

class AuthenticationView(APIView):
    
    def post(self, request):
        serializers = UserCredentialsSerializer(data=request.data)
        
        if serializers.is_valid():
            
            username = serializers.validated_data.get('username')
            password = serializers.validated_data.get('password')

            url = 'http://10.152.164.94:8000/api/token/'
            data = {
                "email":username,
                "password":password
            }

            response = requests.post(url, json = data)

            print(response.text)

            return Response(response.json())
