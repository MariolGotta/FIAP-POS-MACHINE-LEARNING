from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

chrome_options = Options()

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get('https://www.duckduckgo.com')
time.sleep(5)
search_box = driver.find_element(By.NAME, 'q')
search_query = 'Pos Tech FIAP'
time.sleep(5)
search_box.send_keys(search_query)
search_box.submit()
time.sleep(5)
titles = driver.find_elements(By.TAG_NAME, 'h3')
print(f"Resultados para a pesquisa: '{search_query}'\n")
for idx, title in enumerate(titles, start=1):
    print(f"{idx}. {title.text}")
driver.quit()
