import json
import requests

from django.http import JsonResponse
from requests import request
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Librital
from .serializers import LibritalSerializer


class LibritalViewSet(viewsets.ModelViewSet):
    queryset = Librital.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = LibritalSerializer
