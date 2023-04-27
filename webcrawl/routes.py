from flask import Flask, render_template, request, redirect, jsonify
from app import app, login_required, roles_required, db
import asyncio, aiohttp, re, json, uuid, requests, os
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time, json
DEFAULT_REQUEST_HEADERS = {
   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
   "Accept-Language": "en",
   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}
DOWNLOAD_DELAY = 2

async def get_crawl(crawl,linkstore):
    async with aiohttp.ClientSession() as session:
        async with session.get(crawl['link_url'], headers=DEFAULT_REQUEST_HEADERS) as response:
            html = await response.text()
            sel = Selector(text=html)
            datas = sel.response.css(crawl['selector_frame'])
            results = []
            for data in datas:
                item = {
                    '_id': uuid.uuid4().hex,
                    'name': data.css(crawl['selector_name']).get(),
                    'link_url': data.css(crawl['selector_url']).get(),
                }
                if item['name'] or item['link_url']:
                    if not 'https' in item['link_url']:
                        item['link_url'] = linkstore + item['link_url']
                    results.append(item)
            return results

async def get_crawl_category():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://cellphones.com.vn', headers=DEFAULT_REQUEST_HEADERS) as response:
            html = await response.text()
            sel = Selector(text=html)
            datas = sel.response.css('.menu-tree>a')
            results = []
            for data in datas:
                item = {
                    'name': data.css('a>.label-item>span::text').get(),
                    'link_url': data.css('a::attr(href)').get(),
                }
                
                if item['link_url'] != '#':
                    results.append(item)
            return results

async def get_crawl_product_detail(crawl):
    async with aiohttp.ClientSession() as session:
        async with session.get(crawl['link_url'], headers=DEFAULT_REQUEST_HEADERS) as response:
            html = await response.text()
            sel = Selector(text=html)
            datas = sel.response.css('.block-detail-product')
            for data in datas:
                price = data.css('.product__price--show::text').get()
                item = {
                    'product_id': crawl['_id'],
                    'price': ''.join(re.findall(r'\d+', price)),
                    'link_image': data.css('.box-ksp>img::attr(src)').get(),
                    'rating': data.css('.boxReview-score>p::text').get(),
                    'total_rating': data.css('.boxReview-score>p>strong::text').get()
                    # 'description': data.css('.technical-content').get()
                }
                return item
                   
        await asyncio.sleep(DOWNLOAD_DELAY)
        
async def get_crawl_product_comment(crawl):
    async with aiohttp.ClientSession() as session:
        str = crawl['link_url'].replace(".html", "") + '/review'
        async with session.get(str, headers=DEFAULT_REQUEST_HEADERS) as response:
            html = await response.text()
            sel = Selector(text=html)
            datas = sel.response.css('.boxReview-comment>.boxReview-comment-item')
            results = []
            for data in datas:
                item = {
                    'product_id': crawl['_id'],
                    'comment': data.css('.comment-content>p::text').get(),
                }
                results.append(item)
                
            return results
                   
        await asyncio.sleep(DOWNLOAD_DELAY)

@app.route('/crawl/<id>', methods=['GET'])
@login_required
@roles_required('admin')
def crawl(id):
    crawl = db.crawlproducts.find_one({'_id': id})
    return render_template('adminv2/crawl/crawlproduct/crawl.html',crawl=crawl)

@app.route('/crawl/category', methods=['GET','POST'])
@login_required
@roles_required('admin')
def crawlcategory():
    if request.method == 'GET':
        return render_template('admin/crawl/crawlcategory.html')

@app.route('/crawl/category/show', methods=['GET','POST'])
@login_required
@roles_required('admin')
def crawlcategory_show():
    if request.method == 'POST':
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        data = loop.run_until_complete(get_crawl_category())
        new_list = []

        [new_list.append(item) for item in data if item not in new_list]
        
        if os.path.exists('data.json'):
            with open('data.json', 'w') as outfile:
                json.dump({}, outfile)

        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)
            
        return render_template('admin/crawl/crawlcategoryshow.html',data=new_list)

@app.route('/crawl/show/<id>', methods=['POST'])
@login_required
@roles_required('admin')
def crawlshow(id):
    if request.method == 'POST':
        crawlproduct = db.crawlproducts.find_one({'_id': id})
        store = db.stores.find_one({'_id': crawlproduct['store_id']})
        category = db.categories.find_one({'_id': crawlproduct['category_id']})
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        data = loop.run_until_complete(get_crawl(crawlproduct,store['link_url']))
        
        if os.path.exists('data.json'):
            with open('data.json', 'w') as outfile:
                json.dump({}, outfile)

        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)
    
        return render_template('admin/crawl/showcrawl.html',data=data,crawlproduct=crawlproduct,store=store,category=category)
   
@app.route('/crawl/detail', methods=['GET'])
@login_required
@roles_required('admin')
def crawldetail():
    if request.method == 'GET':
        return render_template('admin/crawl/crawldetail.html')
    
@app.route('/crawl/comment', methods=['GET'])
@login_required
@roles_required('admin')
def crawlcomment():
    if request.method == 'GET':
        return render_template('admin/crawl/crawlcomment.html')

@app.route('/crawl/detail/show', methods=['POST'])
@login_required
@roles_required('admin')
def crawldetail_show():
    if request.method == 'POST':
        store = db.stores.find_one({'name': 'cellphones'})
        data = db.products.find({'store_id': store['_id']})
        datas = []
        for item in data:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(get_crawl_product_detail(item))
            datas.append(result)
        return render_template('admin/crawl/crawldetailshow.html',data=datas)

@app.route('/crawl/comment/show', methods=['POST'])
@login_required
@roles_required('admin')
def crawlcomment_show():
    if request.method == 'POST':
        store = db.stores.find_one({'name': 'cellphones'})
        data = db.products.find({'store_id': store['_id']})
        datas = []
        for item in data:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(get_crawl_product_comment(item))
            datas.append(result)
        return render_template('admin/crawl/crawlcommentshow.html',data=datas)

@app.route('/crawl/selenium/<id>', methods=['POST'])
@login_required
@roles_required('admin')
def crawlselenium(id):
  crawlproduct = db.crawlproducts.find_one({'_id': id})
  store = db.stores.find_one({'_id': crawlproduct['store_id']})
  category = db.categories.find_one({'_id': crawlproduct['category_id']})
  DRIVER_PATH='path/to/chrome'
  options = Options()
  options.headless = True
  driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
  try:
    driver.get(crawlproduct['link_url'])
    if crawlproduct['number_page'] and crawlproduct['selector_load_page']:
        for x in range(int(crawlproduct['number_page'])):
            btn = driver.find_element(By.CSS_SELECTOR,crawlproduct['selector_load_page'])
            if not btn: break
            btn.click()
            time.sleep(3)
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
        data = {
            'name': title.strip().replace('\n', ''),
            'link_url': link_url
        }
        datas.append(data)
    with open('data.json', 'w') as json_file:
        json.dump({}, json_file)
    with open('data.json', 'w') as json_file:
        json.dump(datas, json_file)
    driver.quit()
    return render_template('adminv2/crawl/crawlproduct/show.html',data=datas,crawlproduct=crawlproduct,store=store,category=category)
  except:
    driver.quit()
    return jsonify('crawl không thành công')
@app.route('/crawl/save', methods=['POST'])
@login_required
@roles_required('admin')
def crawlsave():
    category_id = request.values.get('category_id')
    store_id = request.values.get('store_id')
    with open('data.json', 'r') as file:
        data = json.load(file)

    for item in data:
        item['category_id'] = category_id
        item['store_id'] = store_id
    
    if db.products.find_one({'store_id': store_id, 'category_id': category_id}):
        return jsonify('đã crawl sản phẩm này rồi '), 400
    
    if db.products.insert_many(data):
        return redirect('/product/list')
    else:
        return jsonify('đồng bộ không thành công'), 400