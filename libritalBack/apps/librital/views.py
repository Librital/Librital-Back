import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view


# Create your views here.
def obtener_mensaje(request):
    texto_fijo = "Django"
    return JsonResponse({'texto': texto_fijo})


# @csrf_exempt
# @ensure_csrf_cookie
# @api_view(['POST'])
def recibir(request):
    if request.method == 'POST':
        print('Raw data:', request.body)
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        received_data = data.get('mensaje')
        print('Received data:', received_data)
        # Continue processing the received data
        return JsonResponse({'message': 'Data received successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
