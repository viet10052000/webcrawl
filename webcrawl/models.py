from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time, json

def crawl_selenium():
  DRIVER_PATH='path/to/chrome'
  options = Options()
  options.headless = True
  driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
  driver.get("https://fptshop.com.vn/dien-thoai")
  for x in range(3):
    btn = driver.find_element(By.CLASS_NAME,"btn-light")
    if not btn: break
    btn.click()
    time.sleep(3)
  datas = []
  soup = BeautifulSoup(driver.page_source, 'html.parser')
  items = soup.select('.cdt-product')
  for item in items:
    try:
      title = item.select_one('.cdt-product__name').text
    except:
      title = ''
    try:
      link_url = item.select_one('.cdt-product__name').get('href')
    except:
      link_url = ''
    data = {
      'title': title,
      'link': link_url
    }
    datas.append(data)
  with open('data.json', 'w') as json_file:
    json.dump({}, json_file)
  with open('data.json', 'w') as json_file:
    json.dump(datas, json_file)
  driver.quit()