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


class FilePostView(APIView):
    
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    
    def post(self,request, *args, **kwargs):
        
        data = request.data.copy()
        
        user = request.user.id
        
        data['user'] = user
        serializers = FileSerializer(data = data)
        
        if serializers.is_valid():
            #serializers.save()
            print(serializers.data)
            return Response(serializers.data)
        else:
            return Response(serializers.errors)