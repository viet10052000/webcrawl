from flask import render_template, request, redirect, jsonify
from app import app, login_required, roles_required, db
import re, json, uuid, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import uuid
import time, json, math
from dotenv import load_dotenv
load_dotenv()

if os.getenv('LOCAL_DRIVER'):
    from selenium.webdriver.chrome.options import Options
else:
    from selenium.webdriver.firefox.options import Options

@app.route('/crawl/<id>', methods=['GET'])
@login_required
@roles_required('admin','collector')
def crawl(id):
    crawl = db.crawlproducts.find_one({'_id': id})
    store = db.stores.find_one({'_id': crawl['store_id']})
    category = db.categories.find_one({'_id': crawl['category_id']})
    return render_template('adminv2/crawl/crawlproduct/crawl.html',crawl=crawl,store=store['name'],category=category['name'])
    
@app.route('/crawl/detail', methods=['GET'])
@login_required
@roles_required('admin','collector')
def crawldetail():
    if request.method == 'GET':
        return render_template('adminv2/crawl/crawlproductdetail/crawl.html')

@app.route('/crawl/selenium/<id>', methods=['POST'])
@login_required
@roles_required('admin','collector')
def crawlselenium(id):
  crawlproduct = db.crawlproducts.find_one({'_id': id})
  crawlproductdetail = db.crawlproductdetails.find_one({"crawlproduct_id":id})
  store = db.stores.find_one({'_id': crawlproduct['store_id']})
  category = db.categories.find_one({'_id': crawlproduct['category_id']})
  if os.getenv('LOCAL_DRIVER'):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
  else:
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
            price = item.select_one(crawlproduct['selector_price']).text
        except:
            price = ''
        data = {
            '_id': uuid.uuid4().hex,
            'category_id': category["_id"],
            'store_id': store["_id"],
            'name': title,
            'link_image': link_image if link_image else '/static/image_default.jpg',
            'price': int(''.join(re.findall(r'\d+', price))),
            'link_url': link_url,
        }
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
                except AttributeError:
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
    return jsonify('crawl error'), 400

@app.route('/crawl/selenium/save/<id>', methods=['GET'])
@login_required
@roles_required('admin','collector')
def crawlsave(id):
    crawlproduct = db.crawlproducts.find_one({'_id': id})
    store = db.stores.find_one({'_id': crawlproduct['store_id']})
    category = db.categories.find_one({'_id': crawlproduct['category_id']})
    with open('data.json', 'r') as file:
        data = json.load(file)

    for item in data:
        if not item["detail"]: continue
        detail = item["detail"]
        del item["detail"]
        db.products.insert_one(item)
        db.productdetails.insert_one(detail)
    
    with open('data.json', 'w') as json_file:
        json.dump({}, json_file)
    return redirect('/product/list')
