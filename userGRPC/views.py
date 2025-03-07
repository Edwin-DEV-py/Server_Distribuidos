from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
import server_pb2 as grpc_pb2
import server_pb2_grpc as grpc_pb2_grpc
import requests
import grpc
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import jwt

#autenticacion por grpc
class AuthenticationView(APIView):
    
    def post(self, request):
        serializers = UserCredentialsSerializer(data=request.data)
        
        if serializers.is_valid():
            
            username = serializers.validated_data.get('username')
            password = serializers.validated_data.get('password')
            
            #conexion gRPC con el server de usuarios
            
            channel = grpc.insecure_channel('localhost:5001')
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
            
            channel = grpc.insecure_channel('127.0.0.1:50051')
            stub = grpc_pb2_grpc.RegisterServiceStub(channel)
            
            userData = grpc_pb2.UserCredentialsRegister(
                username=username,
                name=name,
                email=email,
                phone=phone,
                password=password
            )
            
            register = stub.RegisterUser(userData)
            
            if register.success:
                return Response({'message': register.mensagge})
            else:
                return Response({'error_message': register.error_message})

        else:
            return Response(serializers.errors, status=400)
            

class VerifyUserView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        print(user)
        
        return Response({"message:": user.username})


#login soap
def loginSoapView(username, password):
    
    serializers = UserCredentialsSerializer(data={'username': username, 'password': password})
    
    if serializers.is_valid():
        
        username = serializers.validated_data.get('username')
        password = serializers.validated_data.get('password')
        
        #conexion gRPC con el server de usuarios
        
        #channel = grpc.insecure_channel('host.docker.internal:5000')
        channel = grpc.insecure_channel('172.171.240.20:50051')
        stub = grpc_pb2_grpc.AuthenticationServiceStub(channel)
        #crear el mensjae
        credentials = grpc_pb2.UserCredentials(username=username,password=password)
        
        #llamar al metodo
        authentication = stub.AuthenticateUser(credentials)
        
        #procesar la respuesta del servidor
        if authentication.success:
            print(authentication.token)
            return {'token': authentication.token}
        
        else:
            return {'error_message': authentication.error_message}
        
    else:
        return serializers.errors
    
def registerSoapView(username, name, email, age, password):
    
    serializers = UserDataSerializer(
        data={
            'username': username,
            'name': name,
            'email': email,
            'age': age, 
            'password': password
            }
        )
    
    if serializers.is_valid():
        username = serializers.validated_data.get('username')
        name = serializers.validated_data.get('name')
        email = serializers.validated_data.get('email')
        age = serializers.validated_data.get('age')
        password = serializers.validated_data.get('password')
        
        
        channel = grpc.insecure_channel('172.171.240.20:50051')
        stub = grpc_pb2_grpc.RegisterServiceStub(channel)
        
        #crear el mensaje
        credentials = grpc_pb2.UserCredentialsRegister(
            username=username,
            name=name,
            email=email,
            age=age,
            password=password
        )
        
        #llamar al metodo
        register = stub.RegisterUser(credentials)
        
        if register.success:
            return {'message': register.mensagge}
        else:
            return {'error_message': register.error_message}
    else:
        return serializers.errors
    
def getUsers():
    
    response = requests.get('http://172.171.240.20:5001/users')
    
    print(requests)