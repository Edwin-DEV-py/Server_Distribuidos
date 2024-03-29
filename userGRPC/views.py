from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from grpc import insecure_channel
import server_pb2 as grpc_pb2
import server_pb2_grpc as grpc_pb2_grpc
import requests
import grpc
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


#autenticacion por grpc
class AuthenticationView(APIView):
    
    def post(self, request):
        serializers = UserCredentialsSerializer(data=request.data)
        
        if serializers.is_valid():
            
            username = serializers.validated_data.get('username')
            password = serializers.validated_data.get('password')
            
            #conexion gRPC con el server de usuarios
            
            channel = grpc.insecure_channel('127.0.0.1:50051')
            stub = grpc_pb2_grpc.AuthenticationServiceStub(channel)

            #crear el mensjae
            credentials = grpc_pb2.UserCredentials(username=username,password=password)
            
            #llamar al metodo
            authentication = stub.AuthenticateUser(credentials)
            
            #procesar la respuesta del servidor
            if authentication.success:
                return Response({'token': authentication.token})
            
            else:
                return Response({'error_message': authentication.error_message})
            
        else:
            return Response(serializers.errors, status=400)
        
class RegisterViewGRPC(APIView):
    
    def post(self, request):
        
        serializers = UserDataSerializer(data=request.data)
        
        if serializers.is_valid():
            username = serializers.validated_data.get('username')
            name = serializers.validated_data.get('name')
            email = serializers.validated_data.get('email')
            phone = serializers.validated_data.get('phone')
            password = serializers.validated_data.get('password')
            
            url = 'http://10.152.164.94:8000/api/register/'
            data = {
                "username":username,
                "name":name,
                "email":email,
                "phone":phone,
                "password":password
            }
            
            response = requests.post(url, json = data)

            print(response.text)

            return Response(response.json())

        return Response(serializers.errors)
            

class VerifyUserView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        print(user)
        
        return Response({"message:": user.username})
