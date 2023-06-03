from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json, time
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)
driver.get("https://cellphones.com.vn/mobile/realme.html")
while True:
  try:
    btn = driver.find_element(By.CSS_SELECTOR,'.more-product')
    btn.click()
    time.sleep(3)
  except:
    break
soup = BeautifulSoup(driver.page_source, 'html.parser')
print(soup)
items = soup.select('.lts-product>.item')
datas=[]
comment = 0
for item in items:
  try:
      title = item.select_one('.info>a').text
  except:
      title = ''
  data = {
    'name': title.strip().replace('\n', ''),
  }
  comment += 1
  datas.append(data)
print(datas)
print(comment)
driver.quit()
