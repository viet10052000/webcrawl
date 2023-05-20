from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json, time, re
DRIVER_PATH='path/to/geckodriver'
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path=DRIVER_PATH)
driver.get("https://tiki.vn/search?q=iphone&brand=17827")
soup = BeautifulSoup(driver.page_source, 'html.parser')
items = soup.select('.CatalogProducts__Wrapper-sc-1hmhz3p-0')
print(items)
for item in items:
        try:
            title = item.select_one('.name').text
        except:
            title = ''
        try:
            link_url = item.select_one('.product-item').get('href')
            # if not store['link_url'] in link_url: 
            #     link_url = store['link_url'] + link_url
        except:
            link_url = ''
        try:
            string = str(item.select_one('.webpimg-container img'))
            start_index = string.find('data-src="')
            start_index_src = string.find('src="')
            if start_index != -1:
                start_index += len('data-src="')
                end_index = string.find('"', start_index)
                link_image = string[start_index:end_index]
            else:
                start_index_src += len('src="')
                end_index = string.find('"', start_index_src)
                link_image = string[start_index_src:end_index]
        except:
            link_image = ''
        try:
            price = item.select_one('.price-discount__price').text
        except:
            price = ''
        data = {
            'name': title.strip().replace("\n", ""),
            'link_image': link_image,
            'price': ''.join(re.findall(r'\d+', price)),
            'link_url': link_url,
        }
        print(data)
driver.quit()

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

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup
# import json, time, re
# DRIVER_PATH='path/to/chrome'
# options = Options()
# options.headless = True
# driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
# driver.get("https://fptshop.com.vn/dien-thoai/iphone-14-pro-max")
# # btn_description = driver.find_element(By.CSS_SELECTOR,'button.button__show-modal-technical')
# # btn_description.click()
# soup = BeautifulSoup(driver.page_source, 'html.parser')
# items = soup.select('.st-pd-content p')
# description = ''
# introduction = {}
# rating = 0
# total_rating = 0
# for item in items:
#   description += item.text
# items = soup.select('.st-pd-table tr')
# for item in items:
#   name = item.select_one('td:nth-child(1)').text
#   detail = item.select_one('td:nth-child(2)').text
#   introduction[name] = detail
# rating = soup.select_one('.star div.f-s-ui-44').text
# total_rating = soup.select_one('.star div.m-t-4.text').text
# data = {
#   "description": description,
#   "introduction": introduction,
#   "rating": rating,
#   "total_rating": int(''.join(re.findall(r'\d+', total_rating))),
# }
# print(data)
# driver.quit()

