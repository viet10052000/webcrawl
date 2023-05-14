from flask import Flask, render_template, request, redirect, jsonify
from app import app, login_required, roles_required
from toolcrawl.models import CrawlProduct, CrawlProductDetail
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
        crawl = CrawlProduct().create()
        CrawlProductDetail().create(crawl["_id"])
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
        detail = db.crawlproductdetails.find_one({'crawlproduct_id': id})
        return render_template('adminv2/tool/edit.html',item=item,detail=detail,categories=categories,stores=stores)
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
        }
        detail = db.crawlproductdetails.find_one({'crawlproduct_id': id})
        datadetail = {
            "_id": detail["_id"],
            "selector_price": request.values.get('selector_price'),
            "selector_link_image": request.values.get('selector_link_image'),
            "selector_specification_frame": request.values.get('selector_specification_frame'),
            "selector_specification_name": request.values.get('selector_specification_name'),
            "selector_specification_detail": request.values.get('selector_specification_detail'),
            "selector_specification_button": request.values.get('selector_specification_button'),
            "selector_rating": request.values.get('selector_rating'),
            "selector_total_rating": request.values.get('selector_total_rating'),
            "selector_description": request.values.get('selector_description'),
            "crawlproduct_id": id,
        }
        CrawlProduct().update(id,data)
        CrawlProductDetail().update(detail["_id"], data)
        return redirect('/tool/list')

@app.route('/tool/delete/<id>', methods=['GET'])
@login_required
@roles_required('admin')
def deletetool(id):
    CrawlProduct().delete(id)
    detail = db.crawlproductdetails.find_one({'crawlproduct_id': id})
    CrawlProductDetail().delete(detail["_id"])
    return redirect('/tool/list')