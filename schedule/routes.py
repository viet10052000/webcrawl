from flask import Flask, render_template, request, redirect, jsonify
from app import app, login_required, roles_required, db
from schedule.models import Schedule

@app.route('/schedule/list')
@login_required
@roles_required('admin','collector')
def schedule_list():
    lists = Schedule().index()
    return render_template('/adminv2/schedule/list.html',lists=lists)

@app.route('/schedule/create', methods=['GET','POST'])
@login_required
@roles_required('admin','collector')
def schedule_create():
    if request.method == 'GET':
        categories = list(db.categories.find())
        return render_template('adminv2/schedule/create.html',categories=categories)
    elif request.method == 'POST':
        data = Schedule().create()
        return redirect('/category/list')

@app.route('/schedule/edit/<id>', methods=['GET','POST'])
@login_required
@roles_required('admin','collector')
def schedule_edit(id):
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
        Schedule().update(id,data)
        return redirect('/category/list')
    
@app.route('/schedule/delete/<id>', methods=['GET'])
@login_required
@roles_required('admin','collector')
def schedule_delete(id):
    lists = Schedule().delete(id)
    return redirect('/category/list')