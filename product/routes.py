from flask import render_template, request, redirect, jsonify
from app import app, login_required, roles_required, db
from product.models import Product
from category.models import Category
from math import ceil
from pymongo import ASCENDING
import locale
locale.setlocale(locale.LC_ALL, '')

@app.route('/product/list')
@app.route('/product/list/page/<int:page>')
@login_required
@roles_required('admin')
def productlist(page=1):
    per_page = 10
    skip = (page - 1) * per_page
    total = db.products.count_documents({})
    cursor = db.products.find().sort("field_to_sort", ASCENDING).skip(skip).limit(per_page)
    lists = list(cursor)
    displayed_page_nums = Product().get_displayed_pages(page,int(ceil(total / per_page)),5)
    
    stores = list(db.stores.find())
    categories = list(db.categories.find())
    return render_template('adminv2/product/list.html',lists=lists,pages=displayed_page_nums,current_page=page,stores=stores,categories=categories)

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    categories = Category().index()
    cate = []
    category = []
    for item in categories:
        if not item["parent_id"]:
            cate.append(item)
    for ca in cate:
        child = list(db.categories.find({"parent_id": ca["_id"]}))
        category_item = {
            "_id": ca["_id"],
            "name": ca["name"],
            "image": ca["image"],
            "child": child
        }
        category.append(category_item)
    return render_template("user/home/index.html",category=category)

@app.route('/home/product')
@app.route('/home/product/page/<int:page>')
def home_product(page=1):
    if request.args.get('category'):
        category = db.categories.find_one({"name": request.args.get('category')})
        query = db.products.find({'category_id': category["_id"]})
    elif request.args.get('store'):
        category = db.stores.find_one({"name": request.args.get('store')})
        query = db.products.find({'store_id': category["_id"]})
    else:
        query = db.products.find()
    per_page = 12
    skip = (page - 1) * per_page
    total = db.products.count_documents({})
    cursor = query.sort("field_to_sort", ASCENDING).skip(skip).limit(per_page)
    lists = list(cursor)
    for item in lists:
        item["price"] = locale.format_string("%.0f", int(item["price"]), grouping=True)
    displayed_page_nums = Product().get_displayed_pages(page,int(ceil(total / per_page)),5)
    
    stores = list(db.stores.find())
    categories = list(db.categories.find())
    return render_template("user/product/index.html",lists=lists,pages=displayed_page_nums,current_page=page,stores=stores,categories=categories)

@app.route('/home/product/detail/<id>',methods=['GET'])
def product_detail(id):
    product = db.products.find_one({"_id":id})
    price = product["price"]
    print(price)
    print(int(price) - 1000000)
    print(int(price) + 1000000)
    similar_product = []
    for item in db.products.find({},{"_id":1,"name":1,"price":1,"link_image":1}):
        if int(item["price"]) >= int(price) - 500000 and int(item["price"]) < int(price) + 500000:
            similar_product.append(item)
    product["price"] = locale.format_string("%.0f", int(product["price"]), grouping=True)
    productdetail = db.productdetails.find_one({"product_id": id})
    return render_template("user/product/detail.html",productdetail=productdetail,product=product,similar_product=similar_product)