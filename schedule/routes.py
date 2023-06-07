from flask import Flask, render_template, request, redirect, jsonify
from app import app, login_required, roles_required, db
from schedule.models import Schedule
from datetime import datetime
@app.route('/schedule/list')
@login_required
@roles_required('admin','collector')
def schedule_list():
    lists = Schedule().index()
    for item in lists:
        item["tool"] = db.crawlproducts.find_one({"_id": item["crawlproduct_id"]})
    return render_template('/adminv2/schedule/list.html',lists=lists)

@app.route('/schedule/create', methods=['GET','POST'])
@login_required
@roles_required('admin','collector')
def schedule_create():
    if request.method == 'GET':
        categories = list(db.crawlproducts.find())
        return render_template('adminv2/schedule/create.html',categories=categories)
    elif request.method == 'POST':
        data = Schedule().create()
        return redirect('/schedule/list')

@app.route('/schedule/edit/<id>', methods=['GET','POST'])
@login_required
@roles_required('admin','collector')
def schedule_edit(id):
    if request.method == 'GET':
        category = db.schedules.find_one({ '_id' : id })
        categories = list(db.crawlproducts.find())
        return render_template('adminv2/schedule/edit.html', category=category, categories=categories)
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