from flask import Flask, render_template, request, redirect, jsonify
from app import app, login_required, roles_required, db
from category.models import Category
import uuid, base64
from bson.binary import Binary
@app.route('/category/list')
@login_required
@roles_required('admin')
def categorylist():
    lists = Category().index()
    return render_template('adminv2/category/list.html',lists=lists)

@app.route('/api/category/list')
@login_required
@roles_required('admin')
def api_category_list():
    lists = Category().index()
    return jsonify(lists), 200

@app.route('/category/create', methods=['GET','POST'])
@login_required
@roles_required('admin')
def categorycreate():
    if request.method == 'GET':
        categories = list(db.categories.find())
        return render_template('adminv2/category/create.html',categories=categories)
    elif request.method == 'POST':
        data = Category().create()
        return redirect('/category/list')
    
@app.route('/category/edit/<id>', methods=['GET','POST'])
@login_required
@roles_required('admin')
def categoryedit(id):
    if request.method == 'GET':
        category = db.categories.find_one({ '_id' : id })
        if "image" in category:
            image_base64 = base64.b64encode(category['image']).decode('utf-8')
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
@roles_required('admin')
def categorydelete(id):
    lists = Category().delete(id)
    return redirect('/category/list')