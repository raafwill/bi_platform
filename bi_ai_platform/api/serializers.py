from rest_framework import serializers
from .models import DatabaseConnection, TabelaSemantica
from django.contrib.auth.models import User, Group

class DatabaseConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseConnection
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        client_group, _ = Group.objects.get_or_create(name='Cliente')
        user.groups.add(client_group)
        return user
    
class TabelaSemanticaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabelaSemantica
        fields = '__all__'

class PbitUploadSerializer(serializers.Serializer):
    arquivo = serializers.FileField()