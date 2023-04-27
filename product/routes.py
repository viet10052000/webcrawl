from flask import Flask, render_template, request, redirect, jsonify
from app import app, login_required, roles_required, db
from product.models import Product
from math import ceil
from pymongo import ASCENDING

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