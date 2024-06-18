import os

import cv2
import numpy as np
from PIL import Image
import pytesseract

import nltk
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import words, stopwords

from django.conf import settings
from pytesseract import Output

custom_config = r'--oem 3 --psm 6'

tesseract_path = os.getcwd() + r'\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = tesseract_path


# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

def limpiar_frase(frase):

    tokens = word_tokenize(frase)

    stop_words = set(stopwords.words('spanish'))
    palabras_limpias = [word for word in tokens if word.isalnum() and word.lower() not in stop_words]

    lemmatizer = WordNetLemmatizer()
    lemas = [lemmatizer.lemmatize(word) for word in palabras_limpias]

    frase_limpia = ' '.join(lemas)

    return frase_limpia


def recognizeTextBook(nombre_archivo):
    nombre = nombre_archivo
    image = cv2.imread(settings.MEDIA_ROOT + '\\' + nombre)

    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Denoising
    noise_removal = cv2.medianBlur(gray, 5)
    noise_removal_2 = cv2.medianBlur(image, 7)

    # Aplicar adaptative thresholding
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpen = cv2.filter2D(noise_removal, -1, sharpen_kernel)
    thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # dilation
    kernel_dilation = np.ones((5, 5), np.uint8)
    dilation = cv2.dilate(thresh, kernel_dilation, iterations=1)

    # erosion
    kernel_erosion = np.ones((5, 5), np.uint8)
    erosion = cv2.erode(dilation, kernel_erosion, iterations=1)

    # opening
    kernel_opening = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel_opening)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
    result = 255 - close

    # canny (opcional)
    canny = cv2.Canny(opening, 100, 200)

    # Pre procesado del texto

    cv2.imwrite('ia_media/' + nombre, result)
    imageP = Image.open('ia_media/' + nombre)

    texto_reconodico = pytesseract.image_to_string(imageP, config=custom_config)

    d = pytesseract.image_to_data(imageP, output_type=Output.DICT)

    img = cv2.imread('ia_media/' + nombre)
    n_boxes = len(d['text'])
    for i in range(n_boxes):
        if int(d['conf'][i]) > 60:
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    texto_limpio = limpiar_frase(texto_reconodico.lower())

    return texto_limpio
