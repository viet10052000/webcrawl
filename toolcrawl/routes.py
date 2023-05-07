from flask import Flask, render_template, request, redirect, jsonify
from app import app, login_required, roles_required
from toolcrawl.models import CrawlProduct, CrawlComment, CrawlProductDetail
from app import db

@app.route('/tool/create', methods=['GET','POST'])
@login_required
@roles_required('admin')
def createtool():
    if request.method == 'GET':
        categories = list(db.categories.find())
        stores = list(db.stores.find())
        return render_template('adminv2/tool/create.html',categories=categories,stores=stores)
    elif request.method == 'POST':
        CrawlProduct().create()
        return redirect('/tool/list')

@app.route('/tool/list')
@login_required
@roles_required('admin')
def listtool():
    lists = CrawlProduct().index()
    return render_template('adminv2/tool/list.html',listtool=lists)

@app.route('/tool/edit/<id>', methods=['GET','POST'])
@login_required
@roles_required('admin')
def edittool(id):
    if request.method == 'GET':
        categories = list(db.categories.find())
        stores = list(db.stores.find())
        item = db.crawlproducts.find_one({'_id': id})
        return render_template('adminv2/tool/edit.html',item=item,categories=categories,stores=stores)
    elif request.method == 'POST':
        data = {
            "_id": id,
            "name": request.values.get('name'),
            "category_id": request.values.get('category_id'),
            "store_id": request.values.get('store_id'),
            "link_url": request.values.get('link'),
            "selector_frame": request.values.get('selector_frame'),
            "selector_name": request.values.get('selector_name'),
            "selector_url": request.values.get('selector_url'),
            "selector_load_page": request.values.get('selector_load_page'),
            "number_page": request.values.get('number_page'),
            "status": "no"
        }
        CrawlProduct().update(id,data)
        return redirect('/tool/list')

@app.route('/tool/delete/<id>', methods=['GET'])
@login_required
@roles_required('admin')
def deletetool(id):
    lists = CrawlProduct().delete(id)
    return redirect('/tool/list')

@app.route('/tool/comment/create', methods=['GET','POST'])
@login_required
@roles_required('admin')
def createtoolcomment():
    if request.method == 'GET':
        crawlproducts = list(db.crawlproducts.find())
        return render_template('adminv2/tool/createcomment.html',crawlproducts=crawlproducts)
    elif request.method == 'POST':
        CrawlComment().create()
        return redirect('/tool/list')

@app.route('/tool/comment/list')
@login_required
@roles_required('admin')
def listtoolcomment():
    lists = CrawlComment().index()
    return render_template('adminv2/tool/listcomment.html',listtool=lists)

@app.route('/tool/detail/create', methods=['GET','POST'])
@login_required
@roles_required('admin')
def createtooldetail():
    if request.method == 'GET':
        crawlproducts = list(db.crawlproducts.find())
        return render_template('adminv2/tool/createdetail.html',crawlproducts=crawlproducts)
    elif request.method == 'POST':
        CrawlProductDetail().create()
        return redirect('/tool/list')