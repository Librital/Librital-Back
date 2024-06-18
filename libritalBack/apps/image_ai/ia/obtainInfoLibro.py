import time

import pymysql
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--headless")
options.add_experimental_option('excludeSwitches', ['enable-logging'])


def get_book_cover_image(title):
    conn = pymysql.connect(host='localhost', user='root', password='963963', database='libritalbd')
    cursor = conn.cursor()

    id_libro = 0
    descripcion = ""
    image_url = ""
    titulo = ""
    autor = ""
    categoria = ""
    editorial = ""
    fecha = ""
    isbn13 = ""
    isbn10 = ""

    driver = webdriver.Chrome(options=options)

    driver.get('https://www.casadellibro.com/')

    time.sleep(1)
    cookies_accept = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
    cookies_accept.click()
    time.sleep(1)

    # input_element = driver.find_element(By.CLASS_NAME, 'buscador')
    # input_element.find_element(By.TAG_NAME, 'input').send_keys(title)
    input_element = driver.find_element(By.CLASS_NAME, 'book-finder')
    input_element.send_keys(title)
    input_element.send_keys(Keys.ENTER)

    time.sleep(3)

    try:
        book_card = driver.find_element(By.CLASS_NAME, 'x-result-link')

        try:
            # SI NO ENCUENTRA RESULTADOS
            no_results = driver.find_element(By.CLASS_NAME, 'x-no-results-message')

            if no_results is not None:
                return titulo, autor, editorial, fecha, categoria, isbn13, isbn10, descripcion, 'No encontrado'

        except:

            # SI ENCUENTRA REUSLTADOS
            if book_card is not None:

                link_detail = book_card.get_attribute('href')
                print(link_detail)

                image = driver.find_element(By.CLASS_NAME, 'x-result-picture-image')

                if image is not None:
                    image_url = image.get_attribute('src')

                driver.get(link_detail)
                time.sleep(1)

                listaISBN13 = []
                listaISBN10 = []

                sql_select = "SELECT isbn13, isbn10 FROM libro_libro"

                cursor.execute(sql_select)
                resultadosSelect = cursor.fetchall()

                for i in resultadosSelect:
                    listaISBN13.append(i[0])
                    listaISBN10.append(i[1])

                caracteristicas = driver.find_elements(By.CLASS_NAME, 'spec')

                for caracteristica in caracteristicas:

                    if 'Editorial:' in caracteristica.text:
                        editorial_clean = caracteristica.text.split('\n')[1]
                        editorial = editorial_clean.replace("'", '"')

                    if 'ISBN:' in caracteristica.text:
                        isbn = caracteristica.text.split('\n')[1]

                        if len(isbn) == 13:
                            isbn13 = isbn
                        elif len(isbn) == 10:
                            isbn10 = isbn

                    if 'Fecha de lanzamiento:' in caracteristica.text:
                        fecha = caracteristica.text.split('\n')[1]

                    # Cromprobar si el isbn obtenido existe dentro de la base de datos

                if isbn13 in listaISBN13 or isbn10 in listaISBN10:
                    # EL LIBRO YA EXISTE EN BD

                    titulo_bd = ""
                    autor_bd = ""
                    editorial_bd = ""
                    fecha_bd = ""
                    isbn13_bd = ""
                    isbn10_bd = ""
                    descripcion_bd = ""
                    image_url_bd = ""

                    if isbn13 != "No ISBN" and isbn10 != "No ISBN":

                        if isbn13 != "No ISBN":

                            sql_select_libro = "SELECT id_libro, titulo, autor, editorial, fecha, isbn13, isbn10, descripcion, portada FROM libro_libro WHERE isbn13 = '{0}'".format(
                                isbn13)

                            cursor.execute(sql_select_libro)
                            resultado_libro = cursor.fetchall()

                            for i in resultado_libro:
                                id_libro = i[0]
                                titulo_bd = i[1]
                                autor_bd = i[2]
                                editorial_bd = i[3]
                                fecha_bd = i[4]
                                isbn13_bd = i[5]
                                isbn10_bd = i[6]
                                descripcion_bd = i[7]
                                image_url_bd = i[8]

                            sql_select_categoria_libro = "SELECT id_categoria FROM libro_categoria_libro_categoria WHERE id_libro = {0}".format(
                                id_libro)

                            cursor.execute(sql_select_categoria_libro)
                            resultado_categoria_libro = cursor.fetchone()

                            sql_select_categoria_nombre = "SELECT nombre FROM categoria_categoria WHERE id = {0}".format(
                                resultado_categoria_libro[0])

                            cursor.execute(sql_select_categoria_nombre)
                            categoria_bd = cursor.fetchall()

                            return titulo_bd, autor_bd, editorial_bd, fecha_bd, categoria_bd[
                                0], isbn13_bd, isbn10_bd, descripcion_bd, image_url_bd

                        else:
                            # NO EXISTE ISBN13 PERO SI ISBN10
                            sql_select_libro = "SELECT id_libro, titulo, autor, editorial, fecha, isbn13, isbn10, descripcion, portada FROM libro_libro WHERE isbn10 = '{0}'".format(
                                isbn10)

                            cursor.execute(sql_select_libro)
                            resultado_libro = cursor.fetchall()

                            for i in resultado_libro:
                                titulo_bd = i[0]
                                autor_bd = i[1]
                                editorial_bd = i[2]
                                fecha_bd = i[3]
                                isbn13_bd = i[4]
                                isbn10_bd = i[5]
                                descripcion_bd = i[6]
                                image_url_bd = i[7]

                            sql_select_categoria_libro = "SELECT id_categoria FROM libro_categoria_libro_categoria WHERE id_libro = {0}".format(
                                id_libro)

                            cursor.execute(sql_select_categoria_libro)
                            resultado_categoria_libro = cursor.fetchall()

                            sql_select_categoria_nombre = "SELECT nombre FROM categoria_categoria WHERE id = {0}".format(
                                resultado_categoria_libro[0])
                            cursor.execute(sql_select_categoria_nombre)
                            categoria_bd = cursor.fetchall()


                            return titulo_bd, autor_bd, editorial_bd, fecha_bd, categoria_bd[
                                0], isbn13_bd, isbn10_bd, descripcion_bd, image_url_bd


                    else:
                        # Buscar libro por titulo

                        titulo_ = driver.find_element(By.CLASS_NAME, 'text-h4')
                        if titulo_ is not None:
                            autor_clean = titulo_.text
                            titulo = autor_clean.replace("'", '"')

                        sql_titulo_libro = "SELECT titulo, autor, editorial, fecha, isbn13, isbn10, descripcion, portada FROM libro_libro WHERE titulo LIKE '%'{0}'%'".format(
                            titulo)

                        cursor.execute(sql_titulo_libro)
                        resultado_titulo_libro = cursor.fetchone()

                        if resultado_titulo_libro is not None:
                            titulo_bd = resultado_titulo_libro[0]
                            autor_bd = resultado_titulo_libro[1]
                            editorial_bd = resultado_titulo_libro[2]
                            fecha_bd = resultado_titulo_libro[3]
                            isbn13_bd = resultado_titulo_libro[4]
                            isbn10_bd = resultado_titulo_libro[5]
                            descripcion_bd = resultado_titulo_libro[6]
                            image_url_bd = resultado_titulo_libro[7]

                        else:
                            image_url_bd = "No encontrado"

                        return titulo_bd, autor_bd, editorial_bd, fecha_bd, categoria, isbn13_bd, isbn10_bd, descripcion_bd, image_url_bd

                else:
                    # EL LIBRO NO EXISTE EN BD
                    print('El libro no existe en la base de datos')

                    lista_categoria = driver.find_elements(By.CLASS_NAME, 'cdl-breadcumbs-item')

                    categoria = lista_categoria[2].text

                    descripcion_ = driver.find_elements(By.CLASS_NAME, 'formated-text')

                    if descripcion_ is not None or descripcion_ != "":
                        for i in descripcion_:
                            descripcion_clean = i.text
                            descripcion += descripcion_clean.replace("'", '"')
                    else:
                        descripcion = ""

                    titulo_ = driver.find_element(By.CLASS_NAME, 'text-h4')
                    if titulo_ is not None:
                        autor_clean = titulo_.text
                        titulo = autor_clean.replace("'", '"')

                    autor_ = driver.find_element(By.CLASS_NAME, 'text--darken-1')
                    if autor_ is not None:
                        autor_clean = autor_.text
                        autor = autor_clean.replace("'", '"')

                    return titulo, autor, editorial, fecha, categoria, isbn13, isbn10, descripcion, image_url
            else:
                return titulo, autor, editorial, fecha, categoria, isbn13, isbn10, descripcion, 'No encontrado'
    except:
        return titulo, autor, editorial, fecha, categoria, isbn13, isbn10, descripcion, 'No encontrado'

    driver.quit()
    conn.close()
