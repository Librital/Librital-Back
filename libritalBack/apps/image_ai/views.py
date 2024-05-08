import os.path

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.storage import default_storage

from ..libro.models import Libro

from .ia import coverRecognizer
from .ia import obtainInfoLibro


# Create your views here.


@api_view(['POST'])
def procesarImagenLibro(request):
    if request.method == 'POST':

        imagen = request.FILES['cover']
        nombre_archivo = imagen.name

        titulo = ""
        autor = ""
        editorial = ""
        fecha = ""
        categoria = ""
        isbn13 = ""
        isbn10 = ""
        descripcion = ""
        image_url = ""

        # Guardar el archivo en el sistema de archivos
        with default_storage.open(nombre_archivo, 'wb+') as destino:
            for parte in imagen.chunks():
                destino.write(parte)

        nombre_archivo = default_storage.save(imagen.name, imagen)
        url_imagen = default_storage.url(nombre_archivo)

        texto_limpio = coverRecognizer.recognizeTextBook(nombre_archivo)

        if len(texto_limpio) == 0:
            return Response({'message': 'No encontrado'})

        if len(texto_limpio) > 45:
            texto_limpio = texto_limpio[:45]

        titulo, autor, editorial, fecha, categoria, isbn13, isbn10, descripcion, image_url = obtainInfoLibro.get_book_cover_image(
            texto_limpio)

        if image_url == 'No encontrado':
            return Response({'message': 'No encontrado'})

        else:
            return Response({'message': 'Encontrado',
                             'titulo': titulo,
                             'autor': autor,
                             'editorial': editorial,
                             'fecha': fecha,
                             'categoria': categoria,
                             'isbn13': isbn13,
                             'isbn10': isbn10,
                             'descripcion': descripcion,
                             'image_url': image_url})

        # url_completa = 'http://localhost:8000' + url_imagen
        #
        # imagen_libro = Libro.objects.create(titulo='Libro con imagen', autor='autor prueba', portada=url_completa,
        #                                     isbn13='isbn13', isbn10='isbn10', es_activo=True)
        # imagen_libro.save()
