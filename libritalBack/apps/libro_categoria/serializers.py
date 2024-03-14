from rest_framework import serializers
from .models import libro_Categoria

class libro_CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = libro_Categoria
        fields = '__all__'