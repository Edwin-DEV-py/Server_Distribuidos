from rest_framework.views import APIView
from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from FileApp.forms import FileUploadForm
from .serializers import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
import requests
from rest_framework.renderers import TemplateHTMLRenderer
from django.conf import settings
import jwt
from django.db import transaction
from FolderApp.models import FolderModel
from django.db.models import F

