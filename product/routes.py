from flask import Flask, render_template, request, redirect, jsonify
from app import app, login_required, roles_required, db
from product.models import Product
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
    return render_template("user/home/index.html")
@app.route('/home/product/detail/<int:id>',methods=['GET'])
def product_detail(id):
    print(id)
    if request.method == 'GET':
        producdetail = db.producdetails.find({"product_id": id})
        print(producdetail)
        return render_template("user/product/detail.html")
@app.route('/home/product')
@app.route('/home/product/page/<int:page>')
def home_product(page=1):
    per_page = 12
    skip = (page - 1) * per_page
    total = db.products.count_documents({})
    cursor = db.products.find().sort("field_to_sort", ASCENDING).skip(skip).limit(per_page)
    lists = list(cursor)
    for item in lists:
        item["price"] = locale.format_string("%.0f", int(item["price"]), grouping=True)
    displayed_page_nums = Product().get_displayed_pages(page,int(ceil(total / per_page)),5)
    
    stores = list(db.stores.find())
    categories = list(db.categories.find())
    return render_template("user/product/index.html",lists=lists,pages=displayed_page_nums,current_page=page,stores=stores,categories=categories)