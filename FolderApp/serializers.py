from rest_framework import serializers
from .models import *

class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = FolderModel
        fields = '__all__'
        read_only_fields = ('id','createdAt')