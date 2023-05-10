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
# import json, time
# DRIVER_PATH='path/to/chrome'
# options = Options()
# options.headless = True
# driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
# driver.get("https://viettelstore.vn/dien-thoai/iphone-14-128gb-pid293821.html")
# soup = BeautifulSoup(driver.page_source, 'html.parser')
# items = soup.select('#owl-feature')
# introductions = soup.select('table')
# print(items)
# print(introductions)
# driver.quit()

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup
# import json, time
# DRIVER_PATH='path/to/chrome'
# options = Options()
# options.headless = True
# driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
# driver.get("https://www.thegioididong.com/dtdd/iphone-14-pro-max#2-gia")
# # btn_description = driver.find_element(By.CSS_SELECTOR,'a.btn-show-more')
# # btn_description.click()
# btn_introduction = driver.find_element(By.CSS_SELECTOR,'span.btn-detail.btn-short-spec.not-have-instruction')
# btn_introduction.click()
# soup = BeautifulSoup(driver.page_source, 'html.parser')
# items = soup.select('#productld')
# print(items)
# driver.quit()

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup
# import json, time
# DRIVER_PATH='path/to/chrome'
# options = Options()
# options.headless = True
# driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
# driver.get("https://fptshop.com.vn/dien-thoai/samsung-galaxy-s23-ultra")
# btn_description = driver.find_element(By.CSS_SELECTOR,'a.js--open-modal')
# btn_description.click()
# soup = BeautifulSoup(driver.page_source, 'html.parser')
# items = soup.select('.c-modal__box')
# print(items)
# driver.quit()

