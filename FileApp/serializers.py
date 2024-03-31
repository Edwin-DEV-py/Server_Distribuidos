from rest_framework import serializers
from .models import *

class FileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False)
    
    class Meta:
        model = FileModel
        fields = '__all__'