from flask import Flask, render_template, request, redirect, jsonify
from app import app, login_required, roles_required, db
import asyncio, aiohttp, re, json, uuid, requests, os
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import uuid
import time, json
DRIVER_PATH='path/to/geckodriver'
DEFAULT_REQUEST_HEADERS = {
   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
   "Accept-Language": "en",
   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}
async def get_crawl_category(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=DEFAULT_REQUEST_HEADERS) as response:
            html = await response.text()
            sel = Selector(text=html)
            datas = sel.response.css('.list-brand>a.list-brand__item')
            results = []
            for data in datas:
                link_url =  data.css('a::attr(href)').get(),
                results.append(link_url)
            return results

@app.route('/crawl/<id>', methods=['GET'])
@login_required
@roles_required('admin')
def crawl(id):
    crawl = db.crawlproducts.find_one({'_id': id})
    store = db.stores.find_one({'_id': crawl['store_id']})
    category = db.categories.find_one({'_id': crawl['category_id']})
    return render_template('adminv2/crawl/crawlproduct/crawl.html',crawl=crawl,store=store['name'],category=category['name'])
    
@app.route('/crawl/detail', methods=['GET'])
@login_required
@roles_required('admin')
def crawldetail():
    if request.method == 'GET':
        return render_template('adminv2/crawl/crawlproductdetail/crawl.html')

@app.route('/crawl/selenium/<id>', methods=['POST'])
@login_required
@roles_required('admin')
def crawlselenium(id):
  crawlproduct = db.crawlproducts.find_one({'_id': id})
  crawlproductdetail = db.crawlproductdetails.find_one({"crawlproduct_id":id})
  store = db.stores.find_one({'_id': crawlproduct['store_id']})
  category = db.categories.find_one({'_id': crawlproduct['category_id']})
  options = Options()
  options.headless = True
  driver = webdriver.Firefox(options=options, executable_path=DRIVER_PATH)
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
        except:
            title = ''
        try:
            link_url = item.select_one(crawlproduct['selector_url']).get('href')
            if not store['link_url'] in link_url: 
                link_url = store['link_url'] + link_url
        except:
            link_url = ''
        try:
            link_image = item.select_one(crawlproduct['selector_link_image']).get('src')
        except:
            link_image = ''
        try:
            price = item.select_one(crawlproduct['selector_price']).text
        except:
            price = ''
        data = {
            '_id': uuid.uuid4().hex,
            'category_id': category["_id"],
            'store_id': store["_id"],
            'name': title,
            'link_image': link_image,
            'price': ''.join(re.findall(r'\d+', price)),
            'link_url': link_url,
        }
        datas.append(data)
    for data in datas:
        driver.get(data["link_url"])
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        items = soup.select(crawlproductdetail['selector_description'])
        description = ''
        introduction = {}
        rating = 0
        total_rating = 0
        for item in items:
            description += item.text
        items = soup.select(crawlproductdetail['selector_specification_frame'])
        for item in items:
            name = item.select_one(crawlproductdetail['selector_specification_name']).text
            detail = item.select_one(crawlproductdetail['selector_specification_detail']).text
            introduction[name] = detail
        rating = soup.select_one(crawlproductdetail['selector_rating']).text
        total_rating = soup.select_one(crawlproductdetail['selector_total_rating']).text
        detail = {
            "_id": uuid.uuid4().hex,
            "product_id": data["_id"],
            "description": description,
            "introduction": introduction,
            "rating": rating,
            "total_rating": int(total_rating),
        }
        data["detail"] = detail
    with open('data.json', 'w') as json_file:
        json.dump({}, json_file)
    with open('data.json', 'w') as json_file:
        json.dump(datas, json_file)
    with open('geckodriver.log', 'w') as json_file:
        json.dump({}, json_file)
    driver.quit()    
    return jsonify(datas), 200
  except:
    driver.quit()
    return jsonify('crawl không thành công'), 400

@app.route('/crawl/selenium/save/<id>', methods=['GET'])
@login_required
@roles_required('admin')
def crawlsave(id):
    crawlproduct = db.crawlproducts.find_one({'_id': id})
    store = db.stores.find_one({'_id': crawlproduct['store_id']})
    category = db.categories.find_one({'_id': crawlproduct['category_id']})
    with open('data.json', 'r') as file:
        data = json.load(file)

    for item in data:
        detail = item["detail"]
        del item["detail"]
        db.products.insert_one(item)
        db.productdetails.insert_one(detail)
    
    with open('data.json', 'w') as json_file:
        json.dump({}, json_file)
    return redirect('/product/list')

@app.route('/crawl/brand/test', methods=['GET','POST'])
@login_required
@roles_required('admin')
def branlist():
    if request.method == "GET":
        return render_template("adminv2/crawlv2/show.html")
    elif request.method == "POST":
        data = request.json
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options, executable_path=DRIVER_PATH)
        driver.get(data["url"])
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        items = []
        brand = soup.select(".list-brand__item")
        for item in brand:
            items.append(item.get('href'))
        unique_arr = []
        for i in items:
            if i not in unique_arr:
                unique_arr.append(i)
        # driver.get(items[0])
        # soup = BeautifulSoup(driver.page_source, 'html.parser')
        # items = soup.select_one(".product-item")
        # print(items)
        driver.quit()
        return jsonify(unique_arr), 200
