from rest_framework import serializers
from .models import Libro


class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = '__all__'
        read_only_fields = ['added_at', ]


class LibroCategoriasSerializer(serializers.ModelSerializer):
    nombres_categorias = serializers.ListField(child=serializers.CharField(), read_only=True)

    class Meta:
        model = Libro
        fields = ['id_libro', 'titulo', 'autor', 'portada', 'nombres_categorias',]
        read_only_fields = ['added_at', ]
