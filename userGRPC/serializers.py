from rest_framework import serializers

class UserCredentialsSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()