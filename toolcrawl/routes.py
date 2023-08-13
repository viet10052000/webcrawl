from flask import Flask, render_template, request, redirect, jsonify, flash
from app import app, login_required, roles_required
from toolcrawl.models import CrawlProduct, CrawlProductDetail
import uuid, pymongo
from app import db
from math import ceil
@app.route('/tool/create', methods=['GET','POST'])
@login_required
@roles_required('admin','collector')
def createtool():
    if request.method == 'GET':
        return render_template('adminv2/tool/create.html')
    elif request.method == 'POST':
        data = CrawlProduct().create()
        if 'success' in data:
            flash('Thêm trình thu thập thành công')
            return redirect('/tool/list')
        flash(data)
        return redirect('/tool/create')

@app.route('/tool/list')
@login_required
@roles_required('admin','collector')
def listtool():
    lists = CrawlProduct().index()
    query = {}
    search = dict(request.args)
    page = request.args.get('page', default=1, type=int)
    if request.args.get('category') and request.args.get('store'):
        category = db.categories.find_one({"name": request.args.get('category')},{"_id":1,"name":1,"parent_id":1})
        store = db.stores.find_one({"name": request.args.get('store')})
        if not category["parent_id"]:
            cate = list(db.categories.find({"parent_id": category["_id"]}).distinct('_id'))
            query = {'category_id': {'$in': cate},'store_id': store["_id"]}
        else:
            query = {'category_id': category["_id"],'store_id': store["_id"]}  
    elif request.args.get('category') and not request.args.get('store'):
        category = db.categories.find_one({"name": request.args.get('category')},{"_id":1,"name":1,"parent_id":1})
        if not category["parent_id"]:
            cate = list(db.categories.find({"parent_id": category["_id"]}).distinct('_id'))
            query = {'category_id': {'$in': cate}}
        else:
            query = {'category_id': category["_id"]}
    elif request.args.get('store'):
        store = db.stores.find_one({"name": request.args.get('store')})
        query = {'store_id': store["_id"]}
    elif request.args.get('name'):
        query['name'] = {'$regex': request.args.get('name'), '$options': 'i'}
    else:
        query = {}
    per_page = 10
    skip = (page - 1) * per_page
    total = db.crawlproducts.count_documents(query)
    lists = list(db.crawlproducts.find(query).skip(skip).limit(per_page))
    displayed_page_nums = CrawlProduct().get_displayed_pages(page,int(ceil(total / per_page)),5)
    
    stores = list(db.stores.find())
    categories = list(db.categories.find())
    return render_template('adminv2/tool/list.html',listtool=lists,pages=displayed_page_nums,current_page=page,stores=stores,categories=categories,search=search)

@app.route('/tool/edit/<id>', methods=['GET','POST'])
@login_required
@roles_required('admin','collector')
def edittool(id):
    if request.method == 'GET':
        categories = list(db.categories.find())
        stores = list(db.stores.find())
        item = db.crawlproducts.find_one({'_id': id})
        detail = db.crawlproductdetails.find_one({'crawlproduct_id': id})
        return render_template('adminv2/tool/edittool.html',item=item,detail=detail,categories=categories,stores=stores)
    elif request.method == 'POST':
        # data = {
        #     "name": request.values.get('name'),
        #     "category_id": request.values.get('category_id'),
        #     "store_id": request.values.get('store_id'),
        #     "link_url": request.values.get('link'),
        #     "selector_frame": request.values.get('selector_frame'),
        #     "selector_name": request.values.get('selector_name'),
        #     "selector_url": request.values.get('selector_url'),
        #     "selector_price": request.values.get('selector_price'),
        #     "selector_link_image": request.values.get('selector_link_image'),
        #     "selector_load_page": request.values.get('selector_load_page'),
        # }
        # detail = db.crawlproductdetails.find_one({'crawlproduct_id': id})
        # datadetail = {
        #         "_id": detail["_id"],
        #         "selector_specification_frame": request.values.get('selector_specification_frame'),
        #         "selector_specification_name": request.values.get('selector_specification_name'),
        #         "selector_specification_detail": request.values.get('selector_specification_detail'),
        #         "selector_specification_button": request.values.get('selector_specification_button'),
        #         "selector_rating": request.values.get('selector_rating'),
        #         "selector_total_rating": request.values.get('selector_total_rating'),
        #         "selector_description": request.values.get('selector_description'),
        #         "crawlproduct_id": id,
        # }
        crawlproduct = CrawlProduct().update(id)
        if 'success' in crawlproduct:
            flash('Sửa trình thu thập thành công')
            return redirect('/tool/list')
        flash(crawlproduct)
        return redirect('/tool/edit/' + id)

@app.route('/tool/delete/<id>', methods=['GET'])
@login_required
@roles_required('admin','collector')
def deletetool(id):
    schedule = db.schedules.find_one({'crawlproduct_id': id})
    if (schedule):
        flash('Xóa trình thu thập không thành công. Không thể xóa do liên kết với trình thu thập tự động, hãy xóa tất cả trình thu thập dự động có liên quan trình thu thập này.')
        return redirect('/tool/list')
    detail = db.crawlproductdetails.find_one({'crawlproduct_id': id})
    CrawlProduct().delete(id)
    CrawlProductDetail().delete(detail["_id"])
    if (detail):
        CrawlProduct().delete(id)
        CrawlProductDetail().delete(detail["_id"])
        flash('Xóa trình thu thập thành công')
        return redirect('/tool/list')
    flash('Xóa trình thu thập không thành công')
    return redirect('/tool/list')