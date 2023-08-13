from flask import Flask, render_template, request, redirect, jsonify, flash
from app import app, login_required, roles_required, db
from shop.models import Store

@app.route('/shop/list')
@login_required
@roles_required('admin','collector')
def index():
    lists = Store().index()
    for item in lists:
        item["count"] = db.products.count_documents({"store_id": item["_id"]})
    return render_template('/adminv2/store/list.html',lists=lists)

@app.route('/api/shop/list')
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
        if data == 'success':
            flash('Thêm cửa hàng thành công')
            return redirect('/shop/list')
        flash(data)
        return redirect('/shop/create')
    
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
        store = Store().update(id,data)
        if 'success' in store:
            flash('Sửa cửa hàng thành công.')
            return redirect('/shop/list')
        flash(store)
        return redirect('/shop/edit/' + id)
    
@app.route('/shop/delete/<id>', methods=['GET'])
@login_required
@roles_required('admin','collector')
def delete(id):
    if db.crawlproducts.find_one({'store_id': id}) or db.products.find_one({'store_id': id}):
        data = 'Xóa cửa hàng không thành công. Không thể xóa do còn sản phẩm và trình thu thập dữ liệu liên kết cửa hàng'
        flash(data)
        return redirect('/shop/list')
    lists = Store().delete(id)
    flash('Xóa cửa hàng thành công')
    return redirect('/shop/list')

@app.route('/api/dashboard')
@login_required
@roles_required('admin')
def dashboardapi():
    lists = Store().index()
    for item in lists:
        item["count"] = db.products.count_documents({"store_id": item["_id"]})
    return jsonify(lists), 200

@app.route('/api/dashboard/category')
@login_required
@roles_required('admin')
def dashboardapicate():
    lists = list(db.categories.find({"parent_id":""},{"name":1}))
    for item in lists:
        cate = list(db.categories.find({"parent_id": item["_id"]},{"_id":1}))
        ids = [doc['_id'] for doc in cate]
        item["count"] = db.products.count_documents({"category_id": {"$in": ids}})
    return jsonify(lists), 200

@app.route('/dashboard')
@login_required
@roles_required('admin')
def dashboard():
    total_user = db["users"].count_documents({})
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