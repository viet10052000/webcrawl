from flask import Flask, render_template, request, redirect, jsonify
from app import app, login_required, roles_required, db
from shop.models import Store

@app.route('/shop/list')
@login_required
@roles_required('admin')
def index():
    lists = Store().index()
    return render_template('/adminv2/store/list.html',lists=lists)

@app.route('/shop/create', methods=['GET','POST'])
@login_required
@roles_required('admin')
def create():
    if request.method == 'GET':
        return render_template('/adminv2/store/create.html')
    elif request.method == 'POST':
        data = Store().create()
        return redirect('/shop/list')
    
@app.route('/shop/edit/<id>', methods=['GET','POST'])
@login_required
@roles_required('admin')
def edit(id):
    if request.method == 'GET':
        store = db.stores.find_one({ '_id' : id })
        return render_template('/adminv2/store/edit.html', store=store)
    elif request.method == 'POST':
        data = {
            "_id" : id,
            "name": request.values.get('name'),
            "link_image": request.values.get('link_image'),
            "link_url": request.values.get('link_url')        
        }
        Store().update(id,data)
        return redirect('/shop/list')
    
@app.route('/shop/delete/<id>', methods=['GET'])
@login_required
@roles_required('admin')
def delete(id):
    lists = Store().delete(id)
    return redirect('/shop/list')

@app.route('/dashboard')
@login_required
@roles_required('admin')
def dashboard():
    return render_template('/adminv2/dashboard.html')