
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Inicializa el driver de Chrome
driver = webdriver.Chrome()

# Navega a la página web
driver.get("https://digloservicer.com/listado-productos-yera/todos/todos/todos/todos/todos/todos?field_yera_categoria_target_id=All&field_yera_tipo_producto_target_id=All&field_yera_ubicacion_target_id=&field_yera_referencia_valor_value=")

# Espera hasta que la página se cargue completamente
time.sleep(5)

# Espera hasta que el botón de "Aceptar" del modal de cookies esté presente y haz clic en él
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))).click()

# Inicializa una variable para el scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

# Este conjunto almacenará los enlaces únicos
unique_links = set()

# Este DataFrame almacenará los enlaces para guardarlos en Excel
df = pd.DataFrame(columns=['Links'])

while True:
    # Desplázate hasta el final de la página
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Espera a que se cargue la página
    time.sleep(5)

    # Calcula la nueva altura del scroll y compárala con la última altura
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

    # Encuentra todos los elementos con el xpath dado y extrae los href
    # Asegúrate de que el xpath sea correcto para localizar los enlaces. Esta parte del código puede requerir ajuste en base a la estructura de la página
    elements = driver.find_elements(By.XPATH, '//*[@id="enlaceimagen"]')
    for element in elements:
        href = element.get_attribute("href")
        if href not in unique_links:
            print(href)
            unique_links.add(href)
            df = df._append({'Links': href}, ignore_index=True)

            # Si hemos encontrado 20 propiedades nuevas, guardamos los enlaces en un archivo Excel y vaciamos el DataFrame
            if df.shape[0] % 20 == 0:
                df.to_excel('links.xlsx', index=False)

# Guarda todos los enlaces únicos en el archivo Excel
if not df.empty:
    df.to_excel('links.xlsx', index=False)

# Cierra el driver
driver.quit()



#
# import json
# import xml.etree.ElementTree as ET
# from selenium import webdriver
# from selenium.common import NoSuchElementException, TimeoutException
# from selenium.webdriver.common.by import By
# import pandas as pd
# from datetime import date
# import time
# import re
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import geograpy
#
# # Inicializar el navegador
# driver = webdriver.Chrome()
#
#
#
# # Lee el archivo Excel y obtiene los URLs de la columna "Referencia"
# df = pd.read_excel('properties_data_19.xlsx', sheet_name='Sheet1', usecols=['link'])
#
# # Convierte los URLs en una lista
# url_list = df['link'].tolist()
#
#
# # url_list = ["https://www.solvia.es/es/propiedades/comprar/piso-barcelona-2-dormitorio-110833-174829",
# #             "https://www.solvia.es/es/propiedades/comprar/piso-bell-lloc-durgell-2-dormitorio-71710-157304",
# #             "https://www.solvia.es/es/propiedades/comprar/piso-monovar-monover-3-dormitorio-93893-119688"]
#
# data = []
# counter = 0
# for url in url_list:
#
#     driver.get(url)
#     time.sleep(10)
#
#
#     accept_cookies_button = driver.find_elements(By.CSS_SELECTOR, "a.btn.button_modal.text-center.uppercase")
#     if accept_cookies_button:
#         accept_cookies_button[0].click()
#
#     # # Esperar a que el elemento esté presente en la página antes de extraer el texto
#     # wait = WebDriverWait(driver, 10)
#
#
#     wait = WebDriverWait(driver, 40)
#
#     # provincia
#     try:
#         provincia = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='gallery']/div[2]/div[1]/h1")))
#         provincia_text = provincia.text
#         words = provincia_text.split(',')
#         if len(words) > 3:
#             desired_word_3 = words[3].strip().split(' ')[0]  # split by space and take the first word
#             desired_word_3 = desired_word_3.split('/')[0]  # split by '/' and take the first word
#         else:
#             desired_word_3 = 'N/A'
#     except TimeoutException:
#         desired_word_3 = 'N/A'
#
#     #ciudad
#     try:
#         ciudad = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='gallery']/div[2]/div[1]/h1")))
#         ciudad_text = ciudad.text
#         words = ciudad_text.split(',')
#         if len(words) > 2:
#             desired_word = words[2].strip()  # strip() is used to remove leading and trailing whitespaces
#         else:
#             desired_word = 'N/A'
#     except TimeoutException:
#         desired_word = 'N/A'
#
#     # Metros cuadrados
#     try:
#         metros_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='left-container']/solvia-features/section/div/solvia-features-list/section/div/div[2]/div[1]/h3")))
#
#         metros_text = metros_element.text
#     except TimeoutException:
#         metros_text = 'N/A'
#
#     # Dormitorios
#     try:
#         dormitorio_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='left-container']/solvia-features/section/div/solvia-features-list/section/div/div[2]/div[2]/h3")))
#
#         dormitorio_full_text = dormitorio_element.text
#         dormitorio_numbers = re.findall(r'\d+', dormitorio_full_text)
#         dormitorio_text = ''.join(dormitorio_numbers)
#     except TimeoutException:
#         dormitorio_text = 'N/A'
#
#     # Baños
#     try:
#         bano_element = wait.until(EC.presence_of_element_located((By.XPATH,
#                                                                   "//*[@id='left-container']/solvia-features/section/div/solvia-features-list/section/div/div[2]/div[3]/h3")))
#         bano_full_text = bano_element.text
#         bano_numbers = re.findall(r'\d+', bano_full_text)
#         bano_text = ''.join(bano_numbers)
#     except TimeoutException:
#         bano_text = 'N/A'
#
#
#     # Referencia
#     try:
#         referencia_element = wait.until(EC.presence_of_element_located((By.XPATH,
#                                                                         "//*[@id='left-container']/solvia-features/section/div/solvia-features-list/section/div/div[1]/span[2]")))
#         referencia_full_text = referencia_element.text
#         referencia_match = re.search(r':\s(.*?)\s-', referencia_full_text)
#         referencia_text = referencia_match.group(1) if referencia_match else 'N/A'
#     except TimeoutException:
#         referencia_text = 'N/A'
#
#     # Direccion
#     try:
#         direccion_element = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='propertySheet']/div[1]/solvia-how-is-the-area/section/div[2]/div/span")))
#
#         direccion_text = direccion_element.text
#     except TimeoutException:
#         direccion_text = 'N/A'
#
#     # Título
#     try:
#         title_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='gallery']/div[2]/div[1]/h2")))
#         title_text = title_element.text
#     except:
#         title_text = 'N/A'
#
#
#     # Descripción
#     try:
#         descripcion_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='left-container']/solvia-description/section/div/div[2]/div/span")))
#         descripcion_text = descripcion_element.text
#     except:
#         descripcion_text = 'N/A'
#
#     # Precio
#     try:
#         price_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='gallery']/div[2]/div[2]/div/p[1]/span[2]")))
#         price_text = price_element.text
#     except:
#         price_text = 'N/A'
#
#     # Imagen principal
#     try:
#         main_photo_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='gallery']/solvia-gallery/div/section/div[1]/img")))
#         image_source = main_photo_element.get_attribute("src")
#     except:
#         image_source = 'N/A'
#
#
#     #imprimir todos los valores por consola
#     try:
#         print(f'ciudad: {desired_word}, ref: {referencia_text}, title: {title_text}, direccion: {direccion_text} description: {descripcion_text}, metros: {metros_text}, hab: {dormitorio_text}, baños: {bano_text}, price: {price_text},img: {image_source}, provincia: {desired_word_3}')
#     except BrokenPipeError:
#         print("Error al escribir en el pipe")
#
#     # Almacenar los datos en la lista
#     data.append({
#         "Provincia": desired_word_3,
#         "Ciudad": desired_word,
#         "Referencia": referencia_text,
#         "Title": title_text,
#         "Descripcion": descripcion_text,
#         "Direccion": direccion_text,
#         "MetrosCuadrados": metros_text,
#         "Dormitorios": dormitorio_text,
#         "Baños": bano_text,
#         "Price": price_text,
#         "MainPhoto": image_source,
#
#     })
#
#     # Convertir la lista de datos en un DataFrame
#     df = pd.DataFrame(data, columns=['Referencia', 'Title', 'Descripcion', 'Direccion', 'MetrosCuadrados', 'Dormitorios', 'Baños', 'Price', 'MainPhoto', 'Ciudad', 'Provincia'])
#
#
#     if counter % 20 == 0:
#         file_counter = counter // 20
#         df.to_excel(f"properties_data_{file_counter}.xlsx", index=False, engine="openpyxl")
#
# driver.quit()

