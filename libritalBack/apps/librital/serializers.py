from rest_framework import serializers
from .models import Librital

class LibritalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Librital
        fields = '__all__'
        