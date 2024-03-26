from rest_framework import serializers

class UserCredentialsSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserDataSerializer(serializers.Serializer):
    username = serializers.CharField()
    name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.IntegerField()
    password = serializers.CharField()