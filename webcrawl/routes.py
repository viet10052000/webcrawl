from flask import render_template, request, redirect, jsonify
from app import app, login_required, roles_required, db
import re, json, uuid, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import uuid
import time, json, math
import requests
from datetime import datetime
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}
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

@app.route('/crawl/api', methods=['GET','POST'])
@login_required
@roles_required('admin','collector') 
def crawl_api():
    if request.method == 'GET':
        return render_template('adminv2/crawl/crawlproductapi/index.html')
    elif request.method == 'POST':
        datas = []
        error = ""
        ids = []
        i=0
        for page in range(1,9):
            response = requests.get('https://tiki.vn/api/personalish/v1/blocks/listings?limit=40&include=advertisement&aggregations=2&trackity_id=b5d3ba57-f3a6-fc01-a24e-355a8b7b86f4&category=1789&sort=price,desc&urlKey=dien-thoai-may-tinh-bang&brand=18802&page='+ str(page),headers=headers)
            if response.status_code == 200:
                data = response.json()
                for item in data["data"]:
                    ids.append(str(item["id"]))
                    item = {
                        "_id": item["id"],
                        "name": item["name"],
                        'link_image': item["thumbnail_url"] if item["thumbnail_url"] else '/static/image_default.jpg',
                        'price': item["price"],
                        'link_url': "https://tiki.vn/" + item["url_path"],
                        'detail': {
                            'description': '',
                            'information': {},
                            'rating': item["rating_average"],
                            'total_rating': item["review_count"]
                        }
                    }
                    i = i + 1
                    datas.append(item)
            else:
                error = response.status_code
                print('status code:', response.status_code)
                continue
        if datas:
            return jsonify(ids), 200
        else:
            return jsonify("status code:" + error), 403


@app.route('/crawl/selenium/<id>', methods=['POST'])
@login_required
@roles_required('admin','collector')
def crawlselenium(id):
  crawlproduct = db.crawlproducts.find_one({'_id': id})
  crawlproductdetail = db.crawlproductdetails.find_one({"crawlproduct_id":id})
  store = db.stores.find_one({'_id': crawlproduct['store_id']})
  category = db.categories.find_one({'_id': crawlproduct['category_id']})
#   if os.getenv('LOCAL_DRIVER'):
#     options = Options()
#     options.headless = True
#     driver = webdriver.Chrome(options=options)
#   else:
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
            
            if isinstance(rating, str):
                if "/" in rating:
                    rating = rating.split("/")[0]
                if "," in rating:
                    rating = rating.replace(",", ".").replace("\n", "")
                rating = float(rating)
            if isinstance(total_rating, str):
                numbers = re.findall(r'\d+', total_rating)
                if numbers:
                    total_rating = int(numbers[0])
                else:
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
    if not datas:
        return jsonify('crawl error'), 400 
    return jsonify(datas), 200
  except Exception as e:
    driver.quit()
    return jsonify(e), 400

@app.route('/crawl/selenium/save/<id>', methods=['GET'])
@login_required
@roles_required('admin','collector')
def crawlsave(id):
    with open('data.json', 'r') as file:
        data = json.load(file)

    for item in data:
        if not item["detail"]: continue
        detail = item["detail"]
        del item["detail"]
        item["price_history"] = [
            {
                "price": item["price"],
                "created_at": datetime.now()
            }
        ]
        item["updated_at"] = datetime.now()
        check_duplicate = db.products.find_one({"name": item["name"],"store_id": item["store_id"]})
        if check_duplicate:
            del item["_id"]
            del detail["_id"]
            date_object = check_duplicate["price_history"][0]["created_at"]
            try:
                date_object = datetime.strptime(date_object['$date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                date_object = date_object.strftime('%Y-%m-%d')
            except:
                date_object = date_object.strftime('%Y-%m-%d')
            if datetime.now().strftime('%Y-%m-%d') == date_object:
                item["price_history"] = check_duplicate["price_history"]
            else:
                item["price_history"] = item["price_history"] + check_duplicate["price_history"]
            db.products.update_one({ '_id': check_duplicate['_id'] }, { '$set': item })
            productdetails = db.productdetails.find_one({'product_id': check_duplicate["_id"]},{"_id":1})
            db.productdetails.update_one({'_id': productdetails["_id"]},{ '$set': {
                "description": detail["description"],
                "introduction": detail["introduction"],
                "rating": detail["rating"],
                "total_rating": detail["total_rating"],  
            }})
        else:
            item["created_at"] = datetime.now()
            db.products.insert_one(item)
            db.productdetails.insert_one(detail)
    
    with open('data.json', 'w') as json_file:
        json.dump({}, json_file)
    return redirect('/product/list')
