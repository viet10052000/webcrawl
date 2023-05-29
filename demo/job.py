from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
import concurrent.futures
from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = 'mongodb+srv://user:123456Aa@cluster0.t3aqomt.mongodb.net'
# database
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
db = client.shops
app = Flask(__name__)

scheduler = BackgroundScheduler()
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json, time, math
DRIVER_PATH='path/to/chrome'

# define your job function
def my_job(url):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    items = soup.select('#owl-feature p')
    introductions = soup.select('#panel-cau-hinh table tbody .row_item')
    ratingitem = soup.select(".rating-item .rating-counter")
    total_rating = 0
    i = 5
    count = 0
    description = ''
    avg = 0
    for item in items:
        description += item.text
    for item in ratingitem:
        count += int(item.text)*i
        total_rating += int(item.text)
        i = i - 1
    
    if total_rating != 0:
        avg = math.ceil(count/total_rating)

    intro = {}
    for item in introductions:
        name = item.select_one('.left_row_item').text
        detail = item.select_one('.right_row_item').text
        intro[name] = detail
    
    productdetail = {
        "description" : description,
        "rating_avg" : avg,
        "total_rating" : total_rating,
        "introduction" : intro
    }
    print(productdetail)
    driver.quit()
def start_job():
    start_time = time.perf_counter()
    products = db.products.find_one({ "store_id" : "349d7c6741eb4e248a0842e540ce5954"})
    for item in products:
        my_job(item["link_url"])
    end_time = time.perf_counter()
    print(end_time - start_time)
trigger = DateTrigger(run_date=datetime(2023, 5, 29, 20, 13, 15))
# add the job to the scheduler
scheduler.add_job(start_job, trigger)

# start the scheduler
scheduler.start()

# run the Flask app
if __name__ == '__main__':
    app.run()
