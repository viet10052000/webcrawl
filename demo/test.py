from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json, time, math
DRIVER_PATH='path/to/geckodriver'
def my_job(url):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path=DRIVER_PATH)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    items = soup.select('.lzd-article p')
    introductions = soup.select('.specification-keys .key-li')
    print(introductions)
    # ratingitem = soup.select(".rating-item .rating-counter")
    total_rating = 0
    # i = 5
    # count = 0
    description = ''
    rating = 0
    for item in items:
        description += item.text
    # for item in ratingitem:
    #     count += int(item.text)*i
    #     total_rating += int(item.text)
    #     i = i - 1
    
    # if total_rating != 0:
    #     avg = math.ceil(count/total_rating)

    intro = {}
    for item in introductions:
        try:
            name = item.select_one('.key-title').text
            detail = item.select_one('.key-value').text
            intro[name] = detail
        except AttributeError:
            continue
    
    productdetail = {
        "description" : description,
        "rating_avg" : 0,
        "total_rating" : 0,
        "introduction" : intro
    }
    print(productdetail)
    driver.quit()

my_job("https://www.lazada.vn/products/apple-iphone-14-pro-max-256gb-chinh-hang-vna-i2119599968.html?spm=a2o4n.searchlistbrand.list.1.c5867a2cQjsODL")
