from datetime import datetime
from functools import wraps
from app import db
import os, re, json
import uuid
from apscheduler.schedulers.background import BackgroundScheduler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time, math
from dotenv import load_dotenv
load_dotenv()
scheduler = BackgroundScheduler()
def my_job(jobtimer):
  crawlproduct = db.crawlproducts.find_one({'_id': jobtimer["crawlproduct_id"]})
  crawlproductdetail = db.crawlproductdetails.find_one({"crawlproduct_id": crawlproduct["_id"]})
  store = db.stores.find_one({'_id': crawlproduct['store_id']})
  category = db.categories.find_one({'_id': crawlproduct['category_id']})
  options = Options()
  options.headless = True
  driver = webdriver.Firefox(options=options)
  try:
    driver.get(crawlproduct['link_url'])
    while True:
        try:
            btn = driver.find_element(By.CSS_SELECTOR,crawlproduct['selector_load_page'])
            btn.click()
            time.sleep(4)
        except:
            break
    datas = []
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    items = soup.select(crawlproduct['selector_frame'])
    for item in items:
        try:
            title = item.select_one(crawlproduct['selector_name']).text
            title = title.strip().replace("\n", "")
        except:
            title = ''
        try:
            link_url = item.select_one(crawlproduct['selector_url']).get('href')
            if not store['link_url'] in link_url: 
                link_url = store['link_url'] + link_url
        except:
            link_url = ''
        try:
            string = str(item.select_one(crawlproduct['selector_link_image']))
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
            string = item.select_one(crawlproduct['selector_price']).text
            price = int(''.join(re.findall(r'\d+', string)))
        except:
            price = 0
        data = {
            '_id': uuid.uuid4().hex,
            'category_id': category["_id"],
            'store_id': store["_id"],
            'name': title,
            'link_image': link_image if link_image else '/static/image_default.jpg',
            'price': price,
            'link_url': link_url,
        }
        if link_url:
            datas.append(data)
    for data in datas:
        try:
            driver.get(data["link_url"])
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            items = soup.select(crawlproductdetail['selector_description'])
            description = ''
            introduction = {}
            for item in items:
                description += item.text
            items = soup.select(crawlproductdetail['selector_specification_frame'])
            for item in items:
                try:
                    name = item.select_one(crawlproductdetail['selector_specification_name']).text
                    detail = item.select_one(crawlproductdetail['selector_specification_detail']).text
                    introduction[name] = detail
                except:
                    continue
            try:
                rating = 0
                total_rating = 0
                if crawlproductdetail['selector_total_rating'] == '':
                    i = 5
                    count = 0
                    ratingitem = soup.select(crawlproductdetail['selector_rating'])
                    for item in ratingitem:
                        count += int(item.text)*i
                        total_rating += int(item.text)
                        i = i - 1
                    if total_rating != 0:
                        rating = math.ceil(count/total_rating)
                else:
                    rating = soup.select_one(crawlproductdetail['selector_rating']).text
                    total_rating = soup.select_one(crawlproductdetail['selector_total_rating']).text
            except:
                rating = 0
                total_rating = 0
            detail = {
                "_id": uuid.uuid4().hex,
                "product_id": data["_id"],
                "description": description,
                "introduction": introduction,
                "rating": rating,
                "total_rating": total_rating,
            }       
            data["detail"] = detail
        except:
            data["detail"] = {}
            continue
    print(datas)
    # for item in datas:
    #     if not item["detail"]: continue
    #     detail = item["detail"]
    #     del item["detail"]
        # db.products.insert_one(item)
        # db.productdetails.insert_one(detail)
        # schedule = {
        #     "message": "success",
        #     "status": True,
        #     "total": jobtimer["total"] + 1,
        #     "updated_at": datetime.now(),
        #     "created_at": datetime.now()
        # }
        # db.schedules.update(jobtimer["_id"], { '$set': schedule })
    driver.quit()
  except:
    driver.quit()
    # schedule = {
    #     "message": "error",
    #     "status": False,
    #     "total": jobtimer["total"] + 1,
    #     "updated_at": datetime.now(),
    #     "created_at": datetime.now()
    # }
    # db.schedules.update(jobtimer["_id"], { '$set': schedule })

def start_job():
    schedules = list(db.schedules.find())
    for item in schedules:
        try:
            my_job(item)
        except:
            continue

scheduler.add_job(start_job, 'cron', hour=13, minute=40, second=0)
scheduler.start()
scheduler.print_jobs()