from rest_framework.views import APIView
from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
import requests


class FilePostView(APIView):
    
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    
    def post(self,request, *args, **kwargs):
        
        data = request.data.copy()
        
        user = request.user.id
        
        data['user'] = user
        serializers = FileSerializer(data = data)
        
        if serializers.is_valid():
            """
            response = requests.get('url',json = 'data')
            
            if response.status_code == 200:
                filepath = response.data['paths']
            """
            #serializers.save()
            print(serializers.data)
            return Response(serializers.data)
        else:
            return Response(serializers.errors)
        
class FilesView(APIView):
    
    def get(self,request):
        
        files = FileModel.objects.all()
        serializers = FileSerializer(files, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

