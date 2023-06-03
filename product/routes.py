from flask import render_template, request, redirect, jsonify, g
from app import app, login_required, roles_required, db
from product.models import Product
from category.models import Category
from math import ceil
from pymongo import ASCENDING, DESCENDING
import locale
locale.setlocale(locale.LC_ALL, '')

@app.route('/product/list')
@login_required
@roles_required('admin','collector')
def productlist():
    query = {}
    search = dict(request.args)
    page = request.args.get('page', default=1, type=int)
    if request.args.get('category') and request.args.get('store'):
        category = db.categories.find_one({"name": request.args.get('category')},{"_id":1,"name":1,"parent_id":1})
        store = db.stores.find_one({"name": request.args.get('store')})
        if not category["parent_id"]:
            cate = list(db.categories.find({"parent_id": category["_id"]}).distinct('_id'))
            query = {'category_id': {'$in': cate},'store_id': store["_id"]}
        else:
            query = {'category_id': category["_id"],'store_id': store["_id"]}  
    elif request.args.get('category') and not request.args.get('store'):
        category = db.categories.find_one({"name": request.args.get('category')},{"_id":1,"name":1,"parent_id":1})
        if not category["parent_id"]:
            cate = list(db.categories.find({"parent_id": category["_id"]}).distinct('_id'))
            query = {'category_id': {'$in': cate}}
        else:
            query = {'category_id': category["_id"]}
    elif request.args.get('store'):
        store = db.stores.find_one({"name": request.args.get('store')})
        query = {'store_id': store["_id"]}
    elif request.args.get('name'):
        query['name'] = {'$regex': request.args.get('name'), '$options': 'i'}
    else:
        query = {}
    per_page = 10
    skip = (page - 1) * per_page
    total = db.products.count_documents(query)
    lists = list(db.products.find(query).skip(skip).limit(per_page))
    for item in lists:
        item["store"] = db.stores.find_one({"_id": item["store_id"]})
        item["price"] = locale.format_string("%.0f", int(item["price"]), grouping=True)
    displayed_page_nums = Product().get_displayed_pages(page,int(ceil(total / per_page)),5)
    
    stores = list(db.stores.find())
    categories = list(db.categories.find())
    return render_template('adminv2/product/list.html',lists=lists,pages=displayed_page_nums,current_page=page,stores=stores,categories=categories,search=search)

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return render_template("user/home/index.html",category=g.categories)

@app.route('/home/product')
def home_product():
    query = {}
    page = request.args.get('page', default=1, type=int)
    if request.args.get('category') and request.args.get('store'):
        category = db.categories.find_one({"name": request.args.get('category')},{"_id":1,"name":1,"parent_id":1})
        store = db.stores.find_one({"name": request.args.get('store')})
        if not category["parent_id"]:
            cate = list(db.categories.find({"parent_id": category["_id"]}).distinct('_id'))
            query = {'category_id': {'$in': cate},'store_id': store["_id"]}
        else:
            query = {'category_id': category["_id"],'store_id': store["_id"]}  
    elif request.args.get('category') and not request.args.get('store'):
        category = db.categories.find_one({"name": request.args.get('category')},{"_id":1,"name":1,"parent_id":1})
        if not category["parent_id"]:
            cate = list(db.categories.find({"parent_id": category["_id"]}).distinct('_id'))
            query = {'category_id': {'$in': cate}}
        else:
            query = {'category_id': category["_id"]}
    elif request.args.get('store'):
        store = db.stores.find_one({"name": request.args.get('store')})
        query = {'store_id': store["_id"]}
    elif request.args.get('name'):
        query['name'] = {'$regex': request.args.get('name'), '$options': 'i'}
    else:
        query = {}        
    per_page = 12
    skip = (page - 1) * per_page
    total = db.products.count_documents(query)
    lists = db.products.find(query)
    lists = list(lists.skip(skip).limit(per_page))
    for item in lists:
        item["store"] = db.stores.find_one({"_id": item["store_id"]})
        item["price"] = locale.format_string("%.0f", int(item["price"]), grouping=True)
    displayed_page_nums = Product().get_displayed_pages(page,int(ceil(total / per_page)),5)
    
    stores = list(db.stores.find())
    categories = list(db.categories.find())
    return render_template("user/product/index.html",category=g.categories,lists=lists,pages=displayed_page_nums,current_page=page,stores=stores,categories=categories)

@app.route('/home/product/detail/<id>',methods=['GET'])
def product_detail(id):
    product = db.products.find_one({"_id":id})
    price = product["price"]
    category = db.categories.find_one({"_id": product["category_id"]},{"_id":1,"name":1,"parent_id":1})
    cate = []
    if category["parent_id"]:
        cate = list(db.categories.find({"parent_id": category["parent_id"]}).distinct('_id'))
    similar_product = list(db.products.find({
        'category_id': {'$in': cate},
        "price": {"$gte": price - 500000, "$lt": price + 500000}
    },{
        "_id":1,
        "name":1,
        "price":1,
        "link_image":1,
        "store_id":1
    }))
    for item in similar_product:
        item["store"] = db.stores.find_one({"_id": item["store_id"]})
        item["price"] = locale.format_string("%.0f", int(item["price"]), grouping=True)
    product["price"] = locale.format_string("%.0f", int(product["price"]), grouping=True)
    product["store"] = db.stores.find_one({"_id": product["store_id"]})
    productdetail = db.productdetails.find_one({"product_id": id})
    return render_template("user/product/detail.html",productdetail=productdetail,product=product,similar_product=similar_product)