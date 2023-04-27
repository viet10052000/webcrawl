from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json, os, re
import time
DRIVER_PATH='/path/to/chrome'
options = Options()
options.headless = True

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("https://fptshop.com.vn/may-tinh-xach-tay")
for x in range(8):
  btn = driver.find_element(By.CSS_SELECTOR,".btn-light")
  if not btn:
    break
  btn.click()
  time.sleep(3)
soup = BeautifulSoup(driver.page_source, "html.parser")
items = soup.findAll("div",{ "class": "cdt-product" })
datas = []
for item in items:
    try:
        title = item.find("a",{"class": "cdt-product__name"}).text
    except:
        title = ''
    try:
        link = item.find("a", {"class": "cdt-product__name"}).get('href')
    except:
        link = ''
    data = {'title': title,
            'link': link}
    datas.append(data)
if os.path.exists('data.json'):
  with open('data.json', 'w') as outfile:
    json.dump({}, outfile)

with open('data.json', 'w') as outfile:
  json.dump(datas, outfile)
driver.quit()