from flask import Flask, render_template, request, redirect, jsonify
from app import app, login_required, roles_required, db
from category.models import Category
import uuid, base64, locale
from math import ceil
from bson.binary import Binary
from dotenv import load_dotenv
load_dotenv()
@app.route('/category/list')
@login_required
@roles_required('admin','collector')
def categorylist():
    # lists = Category().index()
    query = {}
    search = dict(request.args)
    page = request.args.get('page', default=1, type=int)
    if request.args.get('name'):
        query['name'] = {'$regex': request.args.get('name'), '$options': 'i'}
    else:
        query = {}
    per_page = 10
    skip = (page - 1) * per_page
    total = db.categories.count_documents(query)
    lists = list(db.categories.find(query).skip(skip).limit(per_page))
    for item in lists:
        if "image" in item:
            try:
                image_base64 = base64.b64decode(item['image']["$binary"]["base64"])
                encoded_image_base64 = base64.b64encode(image_base64).decode('ascii')
                item["image"] = encoded_image_base64
            except:
                image_base64 = base64.b64encode(item['image']).decode('ascii')
                item["image"] = image_base64
    displayed_page_nums = Category().get_displayed_pages(page,int(ceil(total / per_page)),5)
    return render_template('adminv2/category/list.html',lists=lists,pages=displayed_page_nums,current_page=page)

@app.route('/api/category/list')
@login_required
@roles_required('admin','collector')
def api_category_list():
    lists = Category().index()
    return jsonify(lists), 200

@app.route('/category/create', methods=['GET','POST'])
@login_required
@roles_required('admin','collector')
def categorycreate():
    if request.method == 'GET':
        categories = list(db.categories.find())
        return render_template('adminv2/category/create.html',categories=categories)
    elif request.method == 'POST':
        data = Category().create()
        return redirect('/category/list')
    
@app.route('/category/edit/<id>', methods=['GET','POST'])
@login_required
@roles_required('admin','collector')
def categoryedit(id):
    if request.method == 'GET':
        category = db.categories.find_one({ '_id' : id })
        if "image" in category:
            try:
                image_base64 = base64.b64decode(category['image']["$binary"]["base64"])
                encoded_image_base64 = base64.b64encode(image_base64).decode('ascii')
                category["image"] = encoded_image_base64
            except:
                image_base64 = base64.b64encode(category['image']).decode('ascii')
                category["image"] = image_base64
        categories = list(db.categories.find())
        return render_template('adminv2/category/edit.html', category=category, categories=categories)
    elif request.method == 'POST':
        data = {
            "_id" : id,
            "name": request.values.get('name'),
            "description": request.values.get('description'),
            "parent_id": request.values.get('parent_id'),    
        }
        image = request.files['image']
        if image:
            image_data = image.read()
            binary_data = Binary(image_data)
            data["image"] = binary_data
        Category().update(id,data)
        return redirect('/category/list')
    
@app.route('/category/delete/<id>', methods=['GET'])
@login_required
@roles_required('admin','collector')
def categorydelete(id):
    lists = Category().delete(id)
    return redirect('/category/list')