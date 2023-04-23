from flask import Flask, render_template, request, redirect, jsonify
from app import app, login_required, roles_required, db
from category.models import Category

@app.route('/category/list')
@login_required
@roles_required('admin')
def categorylist():
    lists = Category().index()
    return render_template('admin/category/list.html',lists=lists)

@app.route('/category/create', methods=['GET','POST'])
@login_required
@roles_required('admin')
def categorycreate():
    if request.method == 'GET':
        categories = list(db.categories.find())
        return render_template('admin/category/create.html',categories=categories)
    elif request.method == 'POST':
        data = Category().create()
        return redirect('/category/list')
    
@app.route('/category/edit/<id>', methods=['GET','POST'])
@login_required
@roles_required('admin')
def categoryedit(id):
    if request.method == 'GET':
        category = db.categories.find_one({ '_id' : id })
        categories = list(db.categories.find())
        return render_template('admin/category/edit.html', category=category, categories=categories)
    elif request.method == 'POST':
        data = {
            "_id" : id,
            "name": request.values.get('name'),
            "description": request.values.get('description'),
            "parent_id": request.values.get('parent_id'),    
        }
        Category().update(id,data)
        return redirect('/category/list')
    
@app.route('/category/delete/<id>', methods=['GET'])
@login_required
@roles_required('admin')
def categorydelete(id):
    lists = Category().delete(id)
    return redirect('/category/list')