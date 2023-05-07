from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json, time
DRIVER_PATH='path/to/chrome'
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("https://hoanghamobile.com/dien-thoai-di-dong/iphone")
while True:
  try:
    btn = driver.find_element(By.CSS_SELECTOR,'.more-product')
    btn.click()
    time.sleep(3)
  except:
    break
soup = BeautifulSoup(driver.page_source, 'html.parser')
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
