# import re
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import pandas as pd
# import time
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
# page = 0
# # Configurar el web driver
# driver = webdriver.Chrome()
# driver.implicitly_wait(30)  # Aumenta el tiempo de espera implícito a 30 segundos
# driver.get("https://www.solvia.es/es/comprar/viviendas?numeroPagina=" + str(page))
#
# # Aceptar las cookies
# cookies_accept_btn = WebDriverWait(driver, 15).until(
#     EC.element_to_be_clickable((By.XPATH, "//*[@id='solvia-app']/solvia-cookies-policy/solvia-simple-modal[1]/div/div/div[2]/a[1]"))
# )
# cookies_accept_btn.click()
#
# # Recorrer todos los botones "Ver 12 más" y hacer clic en ellos
# counter = 0
#
# href_set = set()
#
# # ... (Importaciones y configuración del webdriver)
#
# # Crea un DataFrame vacío fuera del bucle
# all_properties_data = pd.DataFrame(columns=["link"])
#
# # Itera a través de todas las páginas
# for page in range(399):
#     driver.get("https://www.solvia.es/es/comprar/viviendas?numeroPagina=" + str(page))
#
#     # ... (Aceptar las cookies y esperar a que la página cargue)
#
#     # Encuentra los elementos del título y del precio
#     urls = driver.find_elements(By.XPATH,"//div[@class='col-xs-12']//div/az-element-mosaic/figure/div/div/div/a")
#
#     for url in urls:
#         href = url.get_attribute("href")
#         href_set.add(href)
#
#     # Crea una lista para almacenar los datos de las propiedades
#     properties_data = [{"link": href} for href in href_set]
#
#     # Añade las nuevas propiedades al DataFrame existente
#     all_properties_data = all_properties_data._append(properties_data, ignore_index=True)
#
#     # Elimina las filas duplicadas
#     all_properties_data = all_properties_data.drop_duplicates(subset=["link"], keep="first")
#
#     # Vacía el conjunto href_set para la siguiente página
#     href_set.clear()
#
#     # Guarda el DataFrame en un archivo de Excel cada 20 propiedades
#     if (page + 1) % 20 == 0:
#         file_counter = (page + 1) // 20
#         all_properties_data.to_excel(f"links{file_counter}.xlsx", index=False, engine="openpyxl")
#
# # Cierra el driver de Selenium
# driver.quit()



import json
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import date
import time
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import geograpy
import numpy as np

# Inicializar el navegador
driver = webdriver.Chrome()

# Lee el archivo Excel y obtiene los URLs de la columna "Referencia"
df = pd.read_excel('links_solvia.xlsx', sheet_name='Sheet1', usecols=['link'])

# Convierte los URLs en una lista
url_list = df['link'].tolist()

# Crear un DataFrame vacío para almacenar los datos
all_data = pd.DataFrame(columns=['Referencia', 'Title', 'Descripcion', 'Provincia', 'Direccion',
                                 'MetrosCuadrados', 'Habitaciones',  'Banos', 'Price', 'MainPhoto', 'ImageSources', 'Ciudad'])

# Dividir el DataFrame en lotes para insertar de 100 en 100
batch_size = 100

# Lista para almacenar las propiedades y DataFrames
all_properties = []
data_frames = []


counter = 0
data_batch = []
for url in url_list:

    driver.get(url)
    time.sleep(10)

    accept_cookies_button = driver.find_elements(By.CSS_SELECTOR, "a.btn.button_modal.text-center.uppercase")
    if accept_cookies_button:
        accept_cookies_button[0].click()

    # Esperar a que el elemento esté presente en la página antes de extraer el texto
    wait = WebDriverWait(driver, 40)

    # provincia
    try:
        provincia = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='gallery']/div[2]/div[1]/h1")))
        provincia_text = provincia.text
        words = provincia_text.split(',')
        if len(words) > 3:
            desired_word_3 = words[3].strip().split(' ')[0]  # split by space and take the first word
            desired_word_3 = desired_word_3.split('/')[0]  # split by '/' and take the first word
        else:
            desired_word_3 = 'N/A'
    except TimeoutException:
        desired_word_3 = 'N/A'

    #ciudad
    try:
        ciudad = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='gallery']/div[2]/div[1]/h1")))
        ciudad_text = ciudad.text
        words = ciudad_text.split(',')
        if len(words) > 2:
            desired_word = words[2].strip()  # strip() is used to remove leading and trailing whitespaces
        else:
            desired_word = 'N/A'
    except TimeoutException:
        desired_word = 'N/A'

    # Metros cuadrados
    try:
        metros_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='left-container']/solvia-features/section/div/solvia-features-list/section/div/div[2]/div[1]/h3")))

        metros_text = metros_element.text
    except TimeoutException:
        metros_text = 'N/A'

    # Dormitorios
    try:
        dormitorio_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='left-container']/solvia-features/section/div/solvia-features-list/section/div/div[2]/div[2]/h3")))

        dormitorio_full_text = dormitorio_element.text
        dormitorio_numbers = re.findall(r'\d+', dormitorio_full_text)
        dormitorio_text = ''.join(dormitorio_numbers)
    except TimeoutException:
        dormitorio_text = 'N/A'

    # Baños
    try:
        bano_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='left-container']/solvia-features/section/div/solvia-features-list/section/div/div[2]/div[3]/h3")))
        bano_full_text = bano_element.text
        bano_numbers = re.findall(r'\d+', bano_full_text)
        bano_text = ''.join(bano_numbers)
    except TimeoutException:
        bano_text = 'N/A'

    # Referencia
    try:
        referencia_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='left-container']/solvia-features/section/div/solvia-features-list/section/div/div[1]/span[2]")))
        referencia_full_text = referencia_element.text
        referencia_match = re.search(r':\s(.*?)\s-', referencia_full_text)
        referencia_text = referencia_match.group(1) if referencia_match else 'N/A'
    except TimeoutException:
        referencia_text = 'N/A'

    # Direccion
    try:
        direccion_element = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='propertySheet']/div[1]/solvia-how-is-the-area/section/div[2]/div/span")))

        direccion_text = direccion_element.text
    except TimeoutException:
        direccion_text = 'N/A'

    # Título
    try:
        title_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='gallery']/div[2]/div[1]/h2")))
        title_text = title_element.text
    except:
        title_text = 'N/A'

    # Descripción
    try:
        descripcion_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='left-container']/solvia-description/section/div/div[2]/div/span")))
        descripcion_text = descripcion_element.text
    except:
        descripcion_text = 'N/A'

    # Precio
    try:
        price_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='gallery']/div[2]/div[2]/div/p[1]/span[2]")))
        price_text = price_element.text.replace(' €', '')  # Remover el símbolo de Euro
        price_integer = int(price_text)  # Convertir a un entero
    except:
        price_integer = 'N/A'

    # Imagen principal
    try:
        main_photo_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='gallery']/solvia-gallery/div/section/div[1]/img")))
        image_source = main_photo_element.get_attribute("src")
    except:
        image_source = 'N/A'

    # Crear una lista para almacenar las fuentes de imagen
    image_sources = []

    try:
        main_photo_element_2 = wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='galleryImagenModal']/div/div/div[3]/div[2]/img[1]")))
        image_source_1 = main_photo_element_2.get_attribute("src")
        image_sources.append(image_source_1)
    except:
        image_source_1 = 'N/A'

    try:
        main_photo_element_3 = wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='galleryImagenModal']/div/div/div[3]/div[2]/img[1]")))
        image_source_3 = main_photo_element_3.get_attribute("src")
        image_sources.append(image_source_3)
    except:
        image_source_3 = 'N/A'

    # Convierte la lista de URL en un diccionario y luego en una cadena JSON
    image_sources_dict = {'image_sources': image_sources}
    image_sources_json = json.dumps(image_sources_dict)

    #imprimir todos los valores por consola
    try:
        print(f'ciudad: {desired_word}, ref: {referencia_text}, title: {title_text}, direccion: {direccion_text} description: {descripcion_text}, metros: {metros_text}, hab: {dormitorio_text}, baños: {bano_text}, price: {price_integer},img: {image_source}, provincia: {desired_word_3}, image_sources: {image_sources} ')
    except BrokenPipeError:
        print("Error al escribir en el pipe")

    # Almacenar los datos en el DataFrame y en la lista de lotes
    data_batch.append([
        referencia_text,
        title_text,
        descripcion_text,
        desired_word_3,
        direccion_text,
        metros_text,
        dormitorio_text,
        bano_text,
        price_integer,
        image_source,
        image_sources_json,
        desired_word
    ])
    all_data = all_data._append({
        "Provincia": desired_word_3,
        "Referencia": referencia_text,
        "Title": title_text,
        "Descripcion": descripcion_text,
        "Direccion": direccion_text,
        "MetrosCuadrados": metros_text,
        "Habitaciones": dormitorio_text,
        "Banos": bano_text,
        "Price": price_integer,
        "MainPhoto": image_source,
        "ImageSources": image_sources_json,
        "Ciudad": desired_word
    }, ignore_index=True)

    # Si la lista de lotes tiene 100 elementos, insertarlos en la base de datos
    if len(data_batch) == batch_size:
        data_batch = []

    # Incrementar el contador
    counter += 1

    # Guardar los datos en un archivo xlsx cada 20 propiedades
    if counter % 20 == 0:
        file_counter = counter // 20
        df_temp = pd.DataFrame(all_properties)
        df_temp.to_excel(f"properties_data_{file_counter}.xlsx", index=False, engine="openpyxl")
        all_properties = []

# Guardar los datos en un archivo xlsx al finalizar
df_final = pd.DataFrame(all_properties)
df_final.to_excel("properties_data_all.xlsx", index=False, engine="openpyxl")

driver.quit()
