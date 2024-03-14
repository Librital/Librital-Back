from rest_framework import serializers
from .models import libro_Usuario

class libro_UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = libro_Usuario
        fields = '__all__'
