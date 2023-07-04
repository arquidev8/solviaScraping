import re

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

# ... (Importaciones y configuración del webdriver)

# Crea un DataFrame vacío fuera del bucle
all_properties_data = pd.DataFrame(columns=["link"])

# Itera a través de todas las páginas
for page in range(399):
    driver.get("https://www.solvia.es/es/comprar/viviendas?numeroPagina=" + str(page))

    # ... (Aceptar las cookies y esperar a que la página cargue)

    # Encuentra los elementos del título y del precio
    urls = driver.find_elements(By.XPATH,"//div[@class='col-xs-12']//div/az-element-mosaic/figure/div/div/div/a")
    elementos_provincia = driver.find_elements(By.XPATH,
                                               "//*[@id='busqueda-az__container']/div/div/div/div/div[7]/az-element-mosaic/figure/figcaption/div/div[1]/div/div/div")

    # Iterar sobre los elementos y extraer la primera palabra de cada texto
    for elemento in elementos_provincia:
        texto = elemento.text
        primera_palabra = texto.split()[0]  # Dividir el texto en palabras y tomar la primera palabra

        # Verificar si el caracter '/' está presente en la primera palabra
        if '/' in primera_palabra:
            # Dividir la primera palabra usando el caracter '/'
            partes = re.split(r'\/', primera_palabra)

            # Tomar la primera parte de la lista
            primera_palabra = partes[0]

        print(primera_palabra)
    for url in urls:
        href = url.get_attribute("href")
        href_set.add(href)

    # Crea una lista para almacenar los datos de las propiedades
    properties_data = [{"link": href, "Provincia": primera_palabra} for href in href_set]

    # Añade las nuevas propiedades al DataFrame existente
    all_properties_data = all_properties_data._append(properties_data, ignore_index=True)

    # Elimina las filas duplicadas
    all_properties_data = all_properties_data.drop_duplicates(subset=["link"], keep="first")

    # Vacía el conjunto href_set para la siguiente página
    href_set.clear()

    # Guarda el DataFrame en un archivo de Excel cada 20 propiedades
    if (page + 1) % 20 == 0:
        file_counter = (page + 1) // 20
        all_properties_data.to_excel(f"properties_data_{file_counter}.xlsx", index=False, engine="openpyxl")

# Cierra el driver de Selenium
driver.quit()

# import json
# import xml.etree.ElementTree as ET
# from selenium import webdriver
# from selenium.common import NoSuchElementException
# from selenium.webdriver.common.by import By
# import pandas as pd
# from datetime import date
# import time
# import re
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
# # Función para crear elementos con formato
# def create_element_with_format(root, tag, text=None, level=0):
#     element = ET.SubElement(root, tag)
#     if text is not None:
#         element.text = f"\n{'    ' * level}{text}\n{'    ' * level}"
#     return element
#
# # Inicializar el navegador
# driver = webdriver.Chrome()
#
# cookies_accept_btn = WebDriverWait(driver, 30).until(
#     EC.element_to_be_clickable((By.XPATH, "//*[@id='solvia-app']/solvia-cookies-policy/solvia-simple-modal[1]/div/div/div[2]/a[1]"))
# )
# cookies_accept_btn.click()
#
#
# # # Lista de URLs a extraer
# # url_list = ["https://www.alisedainmobiliaria.com/comprar-vivienda/barcelona/manlleu/52615440",
# #             "https://www.alisedainmobiliaria.com/comprar-vivienda/barcelona/terrassa/51341143",
# #             "https://www.alisedainmobiliaria.com/comprar-vivienda/barcelona/barcelona/37910931"]
#
# # Lee el archivo Excel y obtiene los URLs de la columna "Referencia"
# df = pd.read_excel('properties_data_19.xlsx', sheet_name='Sheet1', usecols=['link'])
#
# # Convierte los URLs en una lista
# url_list = df['link'].tolist()
#
# # Lista para almacenar los datos extraídos de todas las páginas
# data = []
# counter = 0
# # Recorrer cada URL de la lista
# for url in url_list:
#
#     driver.get(url)
#
#     # Obtener los datos de la página
#     referencia = element = driver.find_elements(By.XPATH, "//div[@class='row']/span[2]")
#     try:
#         referencia_text = referencia[0].text
#     except IndexError:
#         print(f"No se encontró el elemento 'referencia' en la URL: {url}")
#         continue
#
#     title = driver.find_elements(By.XPATH, "//div[@class='col-md-8']/h2")
#     try:
#         title_text = title[0].text
#     except IndexError:
#         print(f"No se encontró el elemento 'title' en la URL: {url}")
#         continue
#
#     descripcion = driver.find_elements(By.XPATH, "//div[@class='descriptionContainer']/div[2]/div/span")
#     try:
#         descripcion_text = descripcion[1].text
#     except IndexError:
#         print(f"No se encontró el elemento 'descripcion' en la URL: {url}")
#         continue
#
#     # provincia = driver.find_elements(By.XPATH, "//a[@class='province']")
#     #
#     # try:
#     #     provincia_text = provincia[0].text
#     # except IndexError:
#     #     print(f"No se encontró el elemento 'provincia' en la URL: {url}")
#     #     continue
#
#
#     direccion = driver.find_elements(By.XPATH, "//div[@class='col-xs-12 col-sm-12 col-md-12 col-lg-12 addressDiv']/span")
#     try:
#         direccion_text = direccion[0].text
#     except IndexError:
#         print(f"No se encontró el elemento 'Direccion' en la URL: {url}")
#         continue
#
#     metros_cuadrados = driver.find_elements(By.XPATH, "//div[@class='row sumUpFeatures_div']/div[1]/h3")
#     try:
#         metros_cuadrados_text = metros_cuadrados[0].text
#     except IndexError:
#         print(f"No se encontró el elemento 'metros' en la URL: {url}")
#         continue
#
#     dormitorios = driver.find_elements(By.XPATH,"//div[@class='row sumUpFeatures_div']/div[2]/h3")
#     try:
#         dormitorios_text = dormitorios[0].text
#     except IndexError:
#         print(f"No se encontró el elemento 'dormitorios' en la URL: {url}")
#         continue
#
#     banos = driver.find_elements(By.XPATH, "//div[@class='row sumUpFeatures_div']/div[3]/h3")
#     try:
#         baños_text = banos[0].text
#     except IndexError:
#         print(f"No se encontró el elemento 'baños' en la URL: {url}")
#         continue
#
#
#     price = driver.find_elements(By.XPATH, "//div[@class='foot-aling']/p/span[2]")
#     try:
#         price_text = price[0].text
#     except IndexError:
#         print(f"No se encontró el elemento 'price' en la URL: {url}")
#         continue
#
#     main_photo = driver.find_element(By.XPATH, "//div[@class='item-main']/img")
#     image_source = main_photo.get_attribute("src")
#
#     # Encuentra el contenedor de imágenes
#     image_container = driver.find_elements(By.XPATH, "//div[@class='images-list-modal']/img")
#
#     # # Encuentra todos los elementos de imagen dentro del contenedor
#     # image_elements = image_container.find_elements(By.XPATH, ".//img")
#
#     # Itera sobre los elementos de imagen y extrae el atributo 'src'
#     image_sources = [element.get_attribute("src") for element in image_container]
#
#     image_sources = []
#     # elements = driver.find_elements(By.XPATH,"//div[@class='gallery-grid-right size-4 ng-star-inserted']/div[@class='container_img ng-star-inserted'][position() <= 4]/img")
#     #
#     # for element in elements:
#     #     image_sources.append(element.get_attribute("src"))
#     # try:
#     #     # Esperar hasta que el elemento esté presente en la página
#     #     WebDriverWait(driver,30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.gallery-grid-right.size-4.ng-star-inserted")))
#     #     gallery = driver.find_element(By.CSS_SELECTOR, "div.gallery-grid-right.size-4.ng-star-inserted")
#     #     image_elements = gallery.find_elements(By.CSS_SELECTOR, "div.container_img.ng-star-inserted img")
#     #     image_sources = [element.get_attribute("src") for element in image_elements]
#     # except NoSuchElementException:
#     #     print(f"No se encontró el elemento 'gallery' en la URL: {url}")
#     #     continue
#
#     elements = referencia + descripcion + direccion + title + metros_cuadrados + dormitorios + banos +  price + [image_source] + image_sources
#
#     # Convierte la lista de URL en un diccionario y luego en una cadena JSON
#     image_sources_dict = {'image_sources': image_sources}
#     image_sources_json = json.dumps(image_sources_dict)
#     # Almacenar los datos en la lista
#     data.append({
#         "Referencia": referencia_text,
#         "Title": title_text,
#         "Descripcion": descripcion_text,
#         "Direccion": direccion_text,
#         "MetrosCuadrados": metros_cuadrados_text,
#         "Dormitorios": dormitorios_text,
#         "Baños": baños_text,
#         "Price": price_text,
#         "MainPhoto": image_source,
#         "ImageSources": image_sources
#     })
#
#     # Convertir la lista de datos en un DataFrame
#     df = pd.DataFrame(data, columns=['Referencia', 'Title', 'Descripcion', 'Direccion', 'MetrosCuadrados', 'Dormitorios', 'Baños', 'Price', 'MainPhoto', 'ImageSources'])
#
#
#     # Guarda el DataFrame en un archivo de Excel cada 24 propiedades
#     if counter % 12 == 0:
#         file_counter = counter // 12
#
#         df.to_excel(f"properties_data_{file_counter}.xlsx", index=False, engine="openpyxl")
#
# # Cerrar el navegador
# driver.close()


# import json
# import xml.etree.ElementTree as ET
# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.by import By
# import pandas as pd
# from datetime import date
# import time
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
# # Función para crear elementos con formato
# def create_element_with_format(root, tag, text=None, level=0):
#     element = ET.SubElement(root, tag)
#     if text is not None:
#         element.text = f"\n{'    ' * level}{text}\n{'    ' * level}"
#     return element
#
# def find_element_and_get_text(driver, xpath):
#     try:
#         element = driver.find_element(By.XPATH, xpath)
#         return element.text
#     except NoSuchElementException:
#         print(f"No se encontró el elemento con el XPATH '{xpath}' en la URL: {driver.current_url}")
#         return None
#
# # Inicializar el navegador
# driver = webdriver.Chrome()
#
#
#
#
# # Lee el archivo Excel y obtiene los URLs de la columna "Referencia"
# df = pd.read_excel('properties_data_19.xlsx', sheet_name='Sheet1', usecols=['link'])
#
# # Convierte los URLs en una lista
# url_list = df['link'].tolist()
#
# # Lista para almacenar los datos extraídos de todas las páginas
# data = []
# counter = 0
# # Recorrer cada URL de la lista
# for url in url_list:
#
#     driver.get(url)
#
#     # Aumentar el tiempo de espera a 60 segundos
#     cookies_accept_btn = WebDriverWait(driver, 15).until(
#         EC.presence_of_element_located((By.XPATH, "//div[@class='text-center']//a"))
#     )
#     cookies_accept_btn.click()
#
#     # Obtener los datos de la página
#     referencia_text = find_element_and_get_text(driver, "//div[@class='row']/span[2]")
#     title_text = find_element_and_get_text(driver, "//div[@class='col-md-8']/h2")
#     descripcion_text = find_element_and_get_text(driver, "//div[@class='descriptionContainer']/div[2]/div/span")
#     direccion_text = find_element_and_get_text(driver, "//div[@class='col-xs-12 col-sm-12 col-md-12 col-lg-12 addressDiv']/span")
#     metros_cuadrados_text = find_element_and_get_text(driver, "//div[@class='row sumUpFeatures_div']/div[1]/h3")
#     dormitorios_text = find_element_and_get_text(driver, "//div[@class='row sumUpFeatures_div']/div[2]/h3")
#     baños_text = find_element_and_get_text(driver, "//div[@class='row sumUpFeatures_div']/div[3]/h3")
#     price_text = find_element_and_get_text(driver, "//div[@class='foot-aling']/p/span[2]")
#
#     main_photo = driver.find_element(By.XPATH, "//div[@class='item-main']/img")
#     image_source = main_photo.get_attribute("src")
#
#     # Encuentra el contenedor de imágenes
#     image_container = driver.find_elements(By.XPATH, "//div[@class='images-list-modal']/img")
#
#     # Itera sobre los elementos de imagen y extrae el atributo 'src'
#     image_sources = [element.get_attribute("src") for element in image_container]
#
#     # Convierte la lista de URL en un diccionario y luego en una cadena JSON
#     image_sources_dict = {'image_sources': image_sources}
#     image_sources_json = json.dumps(image_sources_dict)
#
#     # Almacenar los datos en la lista
#     data.append({
#         "Referencia": referencia_text,
#         "Title": title_text,
#         "Descripcion": descripcion_text,
#         "Direccion": direccion_text,
#         "MetrosCuadrados": metros_cuadrados_text,
#         "Dormitorios": dormitorios_text,
#         "Baños": baños_text,
#         "Price": price_text,
#         "MainPhoto": image_source,
#         "ImageSources": image_sources
#     })
#
#     # Convertir la lista de datos en un DataFrame
#     df = pd.DataFrame(data, columns=['Referencia', 'Title', 'Descripcion', 'Direccion', 'MetrosCuadrados', 'Dormitorios', 'Baños', 'Price', 'MainPhoto', 'ImageSources'])
#
#     # Guarda el DataFrame en un archivo de Excel cada 24 propiedades
#     if counter % 12 == 0:
#         file_counter = counter // 12
#
#         df.to_excel(f"properties_data_{file_counter}.xlsx", index=False, engine="openpyxl")
#
# # Cerrar el navegador
# driver.quit()




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
#     # Metros cuadrados
#     try:
#         metros_element = wait.until(EC.presence_of_element_located((By.XPATH,
#                                                                     "//*[@id='left-container']/solvia-features/section/div/solvia-features-list/section/div/div[2]/div[1]/h3")))
#         metros_text = metros_element.text
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
