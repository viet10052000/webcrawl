from flask import Flask, render_template, request, redirect, jsonify
from app import app, login_required, roles_required, db
from shop.models import Store

@app.route('/shop/list')
@login_required
@roles_required('admin','collector')
def index():
    lists = Store().index()
    return render_template('/adminv2/store/list.html',lists=lists)

@app.route('/api/shop/list')
@login_required
@roles_required('admin')
def api_store_list():
    lists = Store().index()
    return jsonify(lists), 200

@app.route('/shop/create', methods=['GET','POST'])
@login_required
@roles_required('admin','collector')
def create():
    if request.method == 'GET':
        return render_template('/adminv2/store/create.html')
    elif request.method == 'POST':
        data = Store().create()
        return redirect('/shop/list')
    
@app.route('/shop/edit/<id>', methods=['GET','POST'])
@login_required
@roles_required('admin','collector')
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
@roles_required('admin','collector')
def delete(id):
    lists = Store().delete(id)
    return redirect('/shop/list')

@app.route('/dashboard')
@login_required
@roles_required('admin','collector')
def dashboard():
    total_user = db["users"].count_documents({"role": "user"})
    total_product = db["products"].count_documents({})
    total_store = db["stores"].count_documents({})
    total_tool = db["crawlproducts"].count_documents({})
    total = {
        "user": total_user,
        "product":total_product,
        "store":total_store,
        "tool":total_tool
    }
    return render_template('/adminv2/dashboard.html',total=total)