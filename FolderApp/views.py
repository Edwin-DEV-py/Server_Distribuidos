from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *


class RegisterFolder(APIView):

    def get(self,request):
        folders = FolderModel.objects.all()
        serializer = FolderSerializer(folders,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):

        serializer = FolderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetFolderByParentId(APIView):

    def get(self,request,parentFolder):
        folder = FolderModel.objects.filter(parentFolder=parentFolder)
        serializer = FolderSerializer(folder, many=True)
        return Response(serializer.data)