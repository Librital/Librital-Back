from django.urls import path
from .views import obtener_mensaje
from .views import recibir

urlpatterns = [
    path('api/obtener_mensaje/', obtener_mensaje, name='obtener_mensaje'),
    path('api/recibir/', recibir, name='recibir')
]
