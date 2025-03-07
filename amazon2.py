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

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--headless")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://www.amazon.com")

try:
    WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Try different image"))
    )
    driver.find_element(By.LINK_TEXT, "Try different image").click()
    time.sleep(3)
except Exception as e:
    pass

try:
    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
    )
    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.send_keys("zapatos")
    search_box.submit()
    time.sleep(1)
except Exception as e:
    print("Error en la barra de busquedas")

try:
    driver.find_element(By.LINK_TEXT, "Skechers").click()
    time.sleep(1)
except Exception as e:
    print("Error en la busqueda de la marca de Zapatos")

try:
    low_price = driver.find_element(By.XPATH, "//*[@id='p_36/range-slider']/form/div[1]/label[1]")
    low_price.click()
    WebDriverWait(driver, 10).until(EC.visibility_of(low_price))

    actions = ActionChains(driver)
    while True:
        current_value = driver.find_element(By.XPATH, "//*[@id='p_36/range-slider_slider-item_lower-bound-slider']").get_attribute('aria-valuetext')
        if current_value != "$100":
            actions.send_keys(Keys.RIGHT).perform()
        else:
            break
except Exception as e:
    print("Error en el slider")

try:
    high_price = driver.find_element(By.XPATH, "//*[@id='p_36/range-slider']/form/div[1]/label[2]")
    high_price.click()
    time.sleep(1)

    actions = ActionChains(driver)
    while True:
        current_value = driver.find_element(By.XPATH, "//*[@id='p_36/range-slider_slider-item_upper-bound-slider']").get_attribute('aria-valuetext')
        if current_value != "$200":
            actions.send_keys(Keys.LEFT).perform()
        else:
            break
except Exception as e:
    print("Error en el slider")

try:
    driver.find_element(By.XPATH, '//*[@id="p_36/range-slider"]/form/div[2]/div[2]').click()
    time.sleep(1)
except Exception as e:
    print("Error en el slider")

try:
    results_text = driver.find_element(By.XPATH, "//*[@id='search']/span/div/h1/div/div[1]/div/h2").text
    print("Texto de resultados:", results_text)
except Exception as e:
    print("Error en el slider")

def print_top_5_products(order):
    try:
        print(f"Los primeros 5 productos ordenados por {order} son:")
        for i, product in enumerate(driver.find_elements(By.XPATH, '//*[@data-index>="2" and @data-index<="7"]')):
            if i >= 5: break
            title = product.find_element(By.XPATH, './/h2')
            try:
                price = product.find_element(By.XPATH, './/span[@class="a-price"]')
                price_text = price.text
            except:
                price_text = "No tiene precio"
            print(f"{i+1}: {title.text} - Precio: {price_text}")
            time.sleep(2)
    except Exception as e:
        print("Error en el texto de resultados")

def click_dropdown(driver):
    try:
        actions = ActionChains(driver)
        dropdown_button = driver.find_element(By.XPATH, '//*[@id="s-result-sort-select"]')
        actions.move_to_element(dropdown_button).click().perform()
    except Exception as e:
        print("No se encontró el dropdown")

# Ordenar de mayor a menor precio
try:
    click_dropdown(driver)
    time.sleep(3)
    actions.move_to_element(driver.find_element(By.XPATH, '//*[@id="s-result-sort-select_2"]')).click().perform()
    time.sleep(3)
    WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@data-index]')))
    print_top_5_products("mayor a menor precio")
except Exception as e:
    print("No se encontró la opcion de Mayor a Menor el dropdown")

# Ordenar por los más recientes
try:
    click_dropdown(driver)
    time.sleep(3)
    actions.send_keys(Keys.DOWN * 2).perform()
    actions.send_keys(Keys.ENTER).perform()
    time.sleep(3)
    WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@data-index]')))
    print_top_5_products("más reciente")
except Exception as e:
    print("No se encontró la opcion de Más recientes en el dropdown")

# Ordenar por promedio de comentarios
try:
    click_dropdown(driver)
    time.sleep(3)
    actions.send_keys(Keys.UP).perform()
    actions.send_keys(Keys.ENTER).perform()
    time.sleep(3)
    WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@data-index]')))
    print_top_5_products("promedio de comentarios de clientes")
except Exception as e:
    print("No se encontró la opcion de Ordenar por promedio de comentarios en el dropdown")

finally:
    driver.quit()
