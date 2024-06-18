import time

import pymysql
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import cryptography

import pandas as pd
from selenium.webdriver.common.keys import Keys

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
    'Accept-Language': 'es'
}

conn = pymysql.connect(host='localhost', user='root', password='963963', database='libritalbd')
cursor = conn.cursor()

url_home = "https://www.casadellibro.com/"

url_categorias = "https://www.casadellibro.com/libros"

driver = webdriver.Chrome()

driver.get(url_categorias)

time.sleep(1)
cookies_accept = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
cookies_accept.click()
time.sleep(1)

pag = requests.get(url_categorias, headers=headers)
soup = BeautifulSoup(pag.content, 'html.parser')

listas_categorias = []


def obtenerLinksCategoria():
    lista_links = soup.find_all('a', class_='text-body-2 accent--text text-underline-hover')

    for link in lista_links:
        listas_categorias.append(url_home + link['href'])



def insertarCategorias():

    driver.get(url_categorias)

    categorias = driver.find_elements(By.CLASS_NAME, 'col-sm-4')

    for i in categorias:
        a = i.find_element(By.TAG_NAME, 'a')
        print(a.text)

        if a.text != "":
            sql = "INSERT INTO categoria_categoria(nombre,descripcion,updated_at,es_activo,img) VALUES ('{0}','{1}',NOW(),{2},'{3}')".format(
                a.text, '', 1, '')

            cursor.execute(sql)
            conn.commit()







def paginacion():
    global card_libros
    isbn13_ = "-1"
    isbn10_ = "-1"
    descripcion_ = ""
    primera = True
    habilitadoBtnNext = True

    lista_categorias_links = soup.find_all('a', class_='text-body-2 accent--text text-underline-hover')

    for i in lista_categorias_links:

        link = i['href']
        # driver.get(url_categorias + link)
        url_categorias = "https://www.casadellibro.com/libros/derecho/109000000"
        driver.get(url_categorias + "\\p24")
        # driver.get(url_categorias + link + "\\p5")
        time.sleep(1)

        btn_pagination = driver.find_element(By.CLASS_NAME, 'v-pagination')
        lista_paginacion = btn_pagination.find_elements(By.TAG_NAME, 'li')

        btn_next = lista_paginacion[-1]

        btn_next_click = btn_next.find_element(By.TAG_NAME, 'button')

        if btn_next_click.is_enabled():
            habilitadoBtnNext = True
        else:
            habilitadoBtnNext = False

        driverDetail = webdriver.Chrome()

        listaISBN13 = []
        listaISBN10 = []

        while habilitadoBtnNext:
            print(driver.current_url)
            if primera is False:

                print("Entra if 2º iteraccion")

                btn_pagination = driver.find_element(By.CLASS_NAME, 'v-pagination')
                lista_paginacion = btn_pagination.find_elements(By.TAG_NAME, 'li')

                btn_next = lista_paginacion[-1]

                btn_next_click = btn_next.find_element(By.TAG_NAME, 'button')

                if btn_next_click.is_enabled():
                    habilitadoBtnNext = True
                    btn_next_click.click()
                else:
                    habilitadoBtnNext = False

                time.sleep(1)
                try:
                    print("Despues de dar click")
                    print(driver.current_url)
                    time.sleep(1)
                    card_libros = driver.find_element(By.CLASS_NAME, 'col-md-9')
                except:
                    print("Entra en el except")
                    driver.refresh()

                if card_libros is not None:

                    lista_libros = card_libros.find_elements(By.CLASS_NAME, 'compact-product')

                    sql_select = "SELECT isbn13, isbn10 FROM libro_libro WHERE id_libro >= 75914"

                    cursor.execute(sql_select)
                    resultados_libros = cursor.fetchall()

                    for i in resultados_libros:
                        listaISBN13.append(i[0])
                        listaISBN10.append(i[1])

                    for card in lista_libros:
                        time.sleep(1)
                        link_detail = card.find_element(By.CLASS_NAME, 'image')
                        link_detail_ = link_detail.get_attribute('href')

                        descripcion = ""
                        image = ""
                        titulo = ""
                        autor = ""
                        editorial = ""
                        fecha = ""
                        isbn13 = "No ISBN"
                        isbn10 = "No ISBN"

                        driverDetail.get(link_detail_)
                        time.sleep(1)

                        caracteristicas = driverDetail.find_elements(By.CLASS_NAME, 'spec')

                        for caracteristica in caracteristicas:

                            if 'Editorial:' in caracteristica.text:
                                editorial_clean = caracteristica.text.split('\n')[1]
                                editorial = editorial_clean.replace("'", '"')

                            if 'ISBN:' in caracteristica.text:
                                isbn = caracteristica.text.split('\n')[1]

                                if len(isbn) == 13:
                                    isbn13 = isbn
                                    isbn13_ = isbn
                                elif len(isbn) == 10:
                                    isbn10 = isbn
                                    isbn10_ = isbn

                            if 'Fecha de lanzamiento:' in caracteristica.text:
                                fecha = caracteristica.text.split('\n')[1]

                        if isbn13_ in listaISBN13:
                            print(isbn13)
                            print("Ya existe")
                        elif isbn10_ in listaISBN10:
                            print(isbn10)
                            print("Ya existe")
                        else:

                            print("No existe")

                            try:
                                descripcion_ = driverDetail.find_element(By.CLASS_NAME, 'formated-text')

                                if descripcion_ is not None or descripcion_ != "":
                                    descripcion_clean = descripcion_.text
                                    descripcion = descripcion_clean.replace("'", '"')

                            except:
                                descripcion = ""

                            link_detail = card.find_element(By.CLASS_NAME, 'image')
                            link_detail = link_detail.get_attribute('href')

                            image_ = card.find_element(By.CLASS_NAME, 'image_content')

                            image__ = image_.find_element(By.TAG_NAME, 'img').get_attribute('src')

                            if image__ is not None or image__ != "":
                                image = image__

                            titulo_ = card.find_element(By.CLASS_NAME, 'compact-product-title').text

                            if titulo_ is not None or titulo_ != "":
                                titulo_clean = titulo_
                                titulo = titulo_clean.replace("'", '"')

                            autor_ = card.find_element(By.CLASS_NAME, 'compact-product-authors').text

                            if autor_ is not None or autor_ != "":
                                autor_clean = autor_
                                autor = autor_clean.replace("'", '"')

                            sql_insert = (
                                "INSERT INTO libro_libro (titulo, autor, editorial, fecha, descripcion, portada, isbn13, isbn10, added_at, updated_at, es_activo) "
                                "VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}',NOW(), NOW(), {8})").format(
                                titulo, autor, editorial, fecha, descripcion, image, isbn13, isbn10, 1)

                            cursor.execute(sql_insert)
                            conn.commit()

            else:

                print("Entra else")
                primera = False

                try:
                    card_libros = driver.find_element(By.CLASS_NAME, 'col-md-9')
                except:
                    driver.refresh()

                if card_libros is not None:

                    lista_libros = card_libros.find_elements(By.CLASS_NAME, 'compact-product')

                    sql_select = "SELECT isbn13, isbn10 FROM libro_libro WHERE id_libro >= 75914"

                    cursor.execute(sql_select)
                    resultados_libros = cursor.fetchall()

                    print(len(resultados_libros))

                    for i in resultados_libros:
                        listaISBN13.append(i[0])
                        listaISBN10.append(i[1])

                    for card in lista_libros:

                        link_detail = card.find_element(By.CLASS_NAME, 'image')
                        link_detail_ = link_detail.get_attribute('href')

                        descripcion = ""
                        image = ""
                        titulo = ""
                        autor = ""
                        editorial = ""
                        fecha = ""
                        isbn13 = "No ISBN"
                        isbn10 = "No ISBN"

                        link_detail = card.find_element(By.CLASS_NAME, 'image')
                        link_detail_ = link_detail.get_attribute('href')

                        driverDetail.get(link_detail_)

                        caracteristicas = driverDetail.find_elements(By.CLASS_NAME, 'spec')

                        for caracteristica in caracteristicas:

                            if 'Editorial:' in caracteristica.text:
                                editorial_clean = caracteristica.text.split('\n')[1]
                                editorial = editorial_clean.replace("'", '"')

                            if 'ISBN:' in caracteristica.text:
                                isbn = caracteristica.text.split('\n')[1]

                                if len(isbn) == 13:
                                    isbn13 = isbn
                                    isbn13_ = isbn
                                elif len(isbn) == 10:
                                    isbn10 = isbn
                                    isbn10_ = isbn

                            if 'Fecha de lanzamiento:' in caracteristica.text:
                                fecha = caracteristica.text.split('\n')[1]


                        if isbn13_ in listaISBN13:
                            print("Ya existe")
                            print(isbn13_)
                        elif isbn10_ in listaISBN10:
                            print("Ya existe")
                            print(isbn10_)
                        else:

                            print("No existe")

                            try:
                                descripcion_ = driverDetail.find_element(By.CLASS_NAME, 'formated-text')

                                if descripcion_ is not None or descripcion_ != "":
                                    descripcion_clean = descripcion_.text
                                    descripcion = descripcion_clean.replace("'", '"')

                            except:
                                descripcion = ""

                            image_ = card.find_element(By.CLASS_NAME, 'image_content')
                            image__ = image_.find_element(By.TAG_NAME, 'img').get_attribute('src')

                            if image__ is not None or image__ != "":
                                image = image__

                            titulo_ = card.find_element(By.CLASS_NAME, 'compact-product-title').text

                            if titulo_ is not None or titulo_ != "":
                                titulo_clean = titulo_
                                titulo = titulo_clean.replace("'", '"')

                            autor_ = card.find_element(By.CLASS_NAME, 'compact-product-authors').text

                            if autor_ is not None or autor_ != "":
                                autor_clean = autor_
                                autor = autor_clean.replace("'", '"')

                            sql_insert = (
                                "INSERT INTO libro_libro (titulo, autor, editorial, fecha, descripcion, portada, isbn13, isbn10, added_at, updated_at, es_activo) "
                                "VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}',NOW(), NOW(), {8})").format(
                                titulo, autor, editorial, fecha, descripcion, image, isbn13, isbn10, 1)

                            cursor.execute(sql_insert)
                            conn.commit()

    primera = True


# insertarCategorias()
paginacion()
