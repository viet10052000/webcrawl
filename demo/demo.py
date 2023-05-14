# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup
# import json, time
# DRIVER_PATH='path/to/chrome'
# options = Options()
# options.headless = True
# driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
# driver.get("https://cellphones.com.vn/iphone-14-pro-max.html")
# soup = BeautifulSoup(driver.page_source, 'html.parser')
# items = soup.select('.modal-content')
# print(items)
# driver.quit()

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup
# import json, time, math
# DRIVER_PATH='path/to/chrome'
# options = Options()
# options.headless = True
# driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
# driver.get("https://viettelstore.vn/dien-thoai/iphone-14-128gb-pid293821.html")
# soup = BeautifulSoup(driver.page_source, 'html.parser')
# items = soup.select('#owl-feature p')
# introductions = soup.select('#panel-cau-hinh table tbody .row_item')
# ratingitem = soup.select(".rating-item .rating-counter")
# total_rating = 0
# i = 5
# count = 0
# for item in items:
#   print(item.text)
# for item in ratingitem:
#   count += int(item.text)*i
#   total_rating += int(item.text)
#   i = i - 1
# print(total_rating)
# print(math.ceil(count/total_rating))
# intro = {}
# for item in introductions:
#   name = item.select_one('.left_row_item').text
#   detail = item.select_one('.right_row_item').text
#   intro[name] = detail
# print(intro)
# driver.quit()

# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup
# import json, time
# DRIVER_PATH='path/to/geckodriver'
# options = Options()
# options.headless = True
# driver = webdriver.Firefox(options=options, executable_path=DRIVER_PATH)
# driver.get("https://cellphones.com.vn/mobile.html")
# driver.get("https://www.thegioididong.com/dtdd/iphone-14-pro-max#2-gia")
# btn_description = driver.find_element(By.CSS_SELECTOR,'a.btn-show-more')
# btn_description.click()
# btn_introduction = driver.find_element(By.CSS_SELECTOR,'span.btn-detail.btn-short-spec.not-have-instruction')
# btn_introduction.click()
# soup = BeautifulSoup(driver.page_source, 'html.parser')
# items = soup.select('.list-brand .list-brand__item')
# for item in items:
#   print(item.get('href'))
# print(items)
# driver.quit()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json, time, re
DRIVER_PATH='path/to/chrome'
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("https://cellphones.com.vn/samsung-galaxy-s23-ultra.html")
btn_description = driver.find_element(By.CSS_SELECTOR,'button.button__show-modal-technical')
btn_description.click()
soup = BeautifulSoup(driver.page_source, 'html.parser')
items = soup.select('.cps-block-content div p')
description = ''
introduction = {}
rating = 0
total_rating = 0
for item in items:
  description += item.text
items = soup.select('.technical-content-modal-item .modal-item-description .is-justify-content-space-between')
for item in items:
  name = item.select_one('p').text
  detail = item.select_one('div').text
  introduction[name] = detail
rating = soup.select_one('.boxReview-score p').text
total_rating = soup.select_one('.boxReview-score strong').text
price = soup.select_one(".box-detail-product__box-center .block-box-price .box-info__box-price .product__price--show").text
link_image = soup.select_one(".box-ksp img").get('src')
data = {
  "description": description,
  "introduction": introduction,
  "rating": re.findall("\d+\.\d+", rating)[0],
  "total_rating": int(total_rating),
  "price": ''.join(re.findall(r'\d+', price)),
  "link_imge": link_image,
}
print(data)
driver.quit()

