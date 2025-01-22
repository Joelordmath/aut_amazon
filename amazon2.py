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
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://www.amazon.com")

try:
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Try different image").click()
    time.sleep(1)

    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.send_keys("zapatos")
    search_box.submit()
    time.sleep(1)

    driver.find_element(By.LINK_TEXT, "Skechers").click()
    time.sleep(1)

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
    time.sleep(1)

    results_text = driver.find_element(By.XPATH, "//*[@id='search']/span/div/h1/div/div[1]/div/h2").text
    print("Texto de resultados:", results_text)

    def print_top_5_products(order):
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
    
    def click_dropdown(driver):
        actions = ActionChains(driver)
        dropdown_button = driver.find_element(By.XPATH, '//*[@id="s-result-sort-select"]')
        actions.move_to_element(dropdown_button).click().perform()        

    # Ordenar de mayor a menor precio
    click_dropdown(driver)
    time.sleep(3)
    actions.move_to_element(driver.find_element(By.XPATH, '//*[@id="s-result-sort-select_2"]')).click().perform()
    time.sleep(3)
    WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@data-index]')))
    print_top_5_products("mayor a menor precio")

    # Ordenar por los más recientes
    click_dropdown(driver)
    time.sleep(3)
    actions.send_keys(Keys.DOWN * 2).perform()  
    actions.send_keys(Keys.ENTER).perform()
    time.sleep(3)
    WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@data-index]')))
    print_top_5_products("más reciente")

    # Ordenar por promedio de comentarios
    click_dropdown(driver)
    time.sleep(3)
    actions.send_keys(Keys.UP).perform()
    actions.send_keys(Keys.ENTER).perform()
    time.sleep(3)
    WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@data-index]')))
    print_top_5_products("promedio de comentarios de clientes")

finally:
    driver.quit()
