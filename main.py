
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

page = 0
# Configurar el web driver
driver = webdriver.Chrome()
driver.implicitly_wait(30)  # Aumenta el tiempo de espera implícito a 30 segundos
driver.get("https://www.solvia.es/es/comprar/viviendas?numeroPagina=" + str(page))

# Aceptar las cookies
cookies_accept_btn = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.XPATH, "//*[@id='solvia-app']/solvia-cookies-policy/solvia-simple-modal[1]/div/div/div[2]/a[1]"))
)
cookies_accept_btn.click()

# Recorrer todos los botones "Ver 12 más" y hacer clic en ellos
counter = 0

href_set = set()
href_list = []

# ... (Importaciones y configuración del webdriver)

# Crea un DataFrame vacío fuera del bucle
all_properties_data = pd.DataFrame(columns=["link"])

# Itera a través de todas las páginas
for page in range(399):

    driver.get("https://www.solvia.es/es/comprar/viviendas?numeroPagina=" + str(page))

    # ... (Aceptar las cookies y esperar a que la página cargue)
    # wait = WebDriverWait(driver, 20)
    # Encuentra los elementos del título y del precio
    try:
        urls = driver.find_elements(By.XPATH,"//div[@class='col-xs-12']//div/az-element-mosaic/figure/div/div/div/a")
    except NoSuchElementException:
        urls = "N/A"

    try:
        provincia = driver.find_elements(By.XPATH, "//*[@id='busqueda-az__container']/div/div/div/div/div[1]/az-element-mosaic/figure/figcaption/div/div[1]/div/div/div/span[2]")
        provincia_text = [p.text.split('/')[0] for p in provincia]
    except NoSuchElementException:
        provincia_text = "N/A"

    try:
        ciudad = driver.find_elements(By.XPATH,  "//*[@id='busqueda-az__container']/div/div/div/div/div[1]/az-element-mosaic/figure/figcaption/div/div[1]/div/div/div/span[3]")
        ciudad_text = [c.text.replace(",", "", 1) for c in ciudad]
    except NoSuchElementException:
        ciudad_text = "N/A"


    # Añade los valores de href a href_list
    for url in urls:
        href = url.get_attribute("href")
        href_list.append(href)

    # Crea una lista para almacenar los datos de las propiedades
    properties_data = []


    # Itera sobre href_list y la lista provincia simultáneamente
    for href, prov, ci in zip(href_list, provincia_text, ciudad_text):
        properties_data.append({"link": href, "Provincia": prov, "Ciudad": ci})

    # Añade la lista properties_data al DataFrame all_properties_data
    all_properties_data = all_properties_data._append(properties_data, ignore_index=True)

    # Elimina las filas duplicadas
    all_properties_data = all_properties_data.drop_duplicates(subset=["link"], keep="first")

    # Limpia href_list para la siguiente página
    href_list.clear()

    # Guarda el DataFrame en un archivo Excel cada 20 propiedades
    if (page + 1) % 20 == 0:
        file_counter = (page + 1) // 20
        all_properties_data.to_excel(f"properties_data_{file_counter}.xlsx", index=False, engine="openpyxl")

# Cierra el driver de Selenium
driver.quit()




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
# df = pd.read_excel('properties_data_1.xlsx', sheet_name='Sheet1', usecols=['link'])
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
#     # Metros cuadrados
#     try:
#         metros_element = wait.until(EC.presence_of_element_located((By.XPATH,
#                                                                     "//*[@id='left-container']/solvia-features/section/div/solvia-features-list/section/div/div[2]/div[1]/h3")))
#         metros_text = metros_element.text.replace("m²", "")
#     except TimeoutException:
#         metros_text = 'N/A'
#
#     # Dormitorios
#     try:
#         dormitorio_element = wait.until(EC.presence_of_element_located((By.XPATH,
#                                                                         "//*[@id='left-container']/solvia-features/section/div/solvia-features-list/section/div/div[2]/div[2]/h3")))
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
#     print(f'ref: {referencia_text}, title: {title_text}, direccion: {direccion_text} description: {descripcion_text}, metros: {metros_text}, hab: {dormitorio_text}, baños: {bano_text}, price: {price_text},img: {image_source}')
#
#     # Almacenar los datos en la lista
#     data.append({
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
#     df = pd.DataFrame(data, columns=['Referencia', 'Title', 'Descripcion', 'Direccion', 'MetrosCuadrados', 'Dormitorios', 'Baños', 'Price', 'MainPhoto', 'Provincia'])
#
#
#     if counter % 20 == 0:
#         file_counter = counter // 20
#
#         df.to_excel(f"properties_data_{file_counter}.xlsx", index=False, engine="openpyxl")
#
# driver.quit()
#
