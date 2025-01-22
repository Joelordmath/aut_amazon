from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configuración del driver
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    driver.get("https://www.amazon.com")

    # Paso 1: Realizar una búsqueda de "zapatos"
    time.sleep(1)
    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.send_keys("zapatos")
    search_box.submit()
    time.sleep(2)

    # Paso 2: Filtrar por la marca "Skechers"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Skechers"))).click()
    time.sleep(2)

    # Paso 3: Elegir rango de precios entre $100 y $200
    actions = ActionChains(driver)
    low_price = driver.find_element(By.XPATH, "//*[@id='p_36/range-slider']/form/div[1]/label[1]")
    low_price.click()
    WebDriverWait(driver, 10).until(EC.visibility_of(low_price))

    while True:
        current_value = driver.find_element(By.XPATH, "//*[@id='p_36/range-slider_slider-item_lower-bound-slider']").get_attribute('aria-valuetext')
        if current_value != "$100":
            actions.send_keys(Keys.RIGHT).perform()
        else:
            break

    high_price = driver.find_element(By.XPATH, "//*[@id='p_36/range-slider']/form/div[1]/label[2]")
    high_price.click()
    time.sleep(1)

    while True:
        current_value = driver.find_element(By.XPATH, "//*[@id='p_36/range-slider_slider-item_upper-bound-slider']").get_attribute('aria-valuetext')
        if current_value != "$200":
            actions.send_keys(Keys.LEFT).perform()
        else:
            break
    time.sleep(2)

    driver.find_element(By.XPATH, '//*[@id="p_36/range-slider"]/form/div[2]/div[2]').click()
    time.sleep(2)

    # Paso 4: Imprimir el número de resultados encontrados
    results_text = driver.find_element(By.XPATH, "//*[@id='search']/span/div/h1/div/div[1]/div/h2").text
    print("Texto de resultados:", results_text)

    # Función para imprimir los primeros 5 productos
    def print_top_5_products(order):
        print(f"Los primeros 5 productos ordenados por {order} son:")
        products = driver.find_elements(By.XPATH, '//*[@data-index]')
        for i, product in enumerate(products[:5]):
            try:
                title = product.find_element(By.XPATH, './/h2').text
                price = product.find_element(By.XPATH, './/span[@class="a-price"]').text
            except NoSuchElementException:
                title = "Título no disponible"
                price = "Precio no disponible"
            print(f"{i + 1}: {title} - Precio: {price}")
        print()

    # Función para manejar el menú desplegable
    def click_dropdown(option_text):
        dropdown = driver.find_element(By.ID, "s-result-sort-select")
        dropdown.click()
        time.sleep(2)
        option = driver.find_element(By.XPATH, f"//option[contains(text(), '{option_text}')]")
        option.click()
        time.sleep(3)

    # Paso 5: Ordenar los productos por "Precio: De más alto a más bajo"
    click_dropdown("Precio: De más alto a más bajo")
    print_top_5_products("Precio: De más alto a más bajo")

    # Paso 8: Ordenar por nuevos lanzamientos
    click_dropdown("Novedades")
    print_top_5_products("Nuevos lanzamientos")

    # Paso 9: Ordenar por promedio de comentarios de clientes
    click_dropdown("Promedio de comentarios de clientes")
    print_top_5_products("Promedio de comentarios de clientes")

except TimeoutException as e:
    print("Error: Se agotó el tiempo de espera.")
    driver.save_screenshot('error_screenshot.png')
    print("Se guardó un screenshot con el nombre 'error_screenshot.png'.")
    raise e
except Exception as e:
    print(f"Error inesperado: {e}")
    driver.save_screenshot('unexpected_error_screenshot.png')
    print("Se guardó un screenshot con el nombre 'unexpected_error_screenshot.png'.")
    raise e
finally:
    driver.quit()
    