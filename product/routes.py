from flask import render_template, request, redirect, jsonify, g, flash
from app import app, login_required, roles_required, db
from product.models import Product
from category.models import Category
from math import ceil
from pymongo import ASCENDING, DESCENDING
import locale, re
import difflib
locale.setlocale(locale.LC_ALL, '')

@app.route('/api/product/detail/<id>')
def api_get_price_history(id):
    product = db.products.find_one({"_id":id})
    return jsonify(product["price_history"]), 200

@app.route('/product/delete/<id>', methods=['GET'])
@login_required
@roles_required('admin','collector')
def deleteproduct(id):
    product = db.products.find_one({'_id': id})
    detail = db.productdetails.find_one({'product_id': id})
    if product:
        db.products.delete_one({'_id': id})
        if detail:
            db.productdetails.delete_one({'_id': detail['_id']})
        flash('Xóa sản phẩm thành công')
        return redirect('/product/list')
    flash('Xóa sản phẩm không thành công')
    return redirect('/product/list')

@app.route('/product/list')
@login_required
@roles_required('admin','collector')
def productlist():
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
    total = db.products.count_documents(query)
    lists = list(db.products.find(query).skip(skip).limit(per_page))
    for item in lists:
        item["store"] = db.stores.find_one({"_id": item["store_id"]})
        if item["price"]:
            item["price"] = locale.format_string("%.0f", int(item["price"]), grouping=True)
    displayed_page_nums = Product().get_displayed_pages(page,int(ceil(total / per_page)),5)
    
    stores = list(db.stores.find())
    categories = list(db.categories.find())
    return render_template('adminv2/product/list.html',lists=lists,pages=displayed_page_nums,current_page=page,stores=stores,categories=categories,search=search)

@app.route('/product/detail/<id>', methods=['GET'])
@login_required
@roles_required('admin','collector')
def get_product_detail(id):
    product = db.products.find_one({"_id":id})
    product['category'] = db.categories.find_one({"_id": product["category_id"]},{"name":1})
    product["store"] = db.stores.find_one({"_id": product["store_id"]},{"name":1})
    product["detail"] = db.productdetails.find_one({"product_id": id})
    return render_template("adminv2/product/detail.html",product=product)
    
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    similar_product = list(db.products.find().limit(10))
    for item in similar_product:
        item["store"] = db.stores.find_one({"_id": item["store_id"]})
        item["price"] = locale.format_string("%.0f", int(item["price"]), grouping=True)
    stores = list(db.stores.find())
    return render_template("user/home/index.html",category=g.categories,stores=stores,similar_product=similar_product)

@app.route('/home/product/compare')
def home_product_compare():
    category = db.categories.find_one({"name": request.args.get('category')},{"_id": 1 })
    ids = list(db.products.find({"category_id": category["_id"]}).distinct("store_id"))
    products = list(db.products.find({"category_id":category["_id"]}))
    tmp = []
    datas = []
    for id in ids:
        list3 = []
        list1 = [obj for obj in products if obj["store_id"] == id]
        if tmp:
            list3 = [a for a in list3 if a in tmp]
        else:
            list3 = list1
        for item in list3:
            data = []
            price = []
            list2 = [obj["name"] for obj in products if obj["store_id"] != id]
            name_compare = item["name"].replace("(", "").replace(")", "").replace("Chính hãng","").replace("VN/A","").replace("-","").strip()
            result = find_longest_common_subarray(name_compare, list2)
            if result:
                for ilist in products:
                    name = is_subarray_in_string(result,ilist["name"])
                    if name:
                        data.append(ilist)
                        tmp.append(ilist["name"])
                        price.append(ilist["price"])
            if data:
                data_compare = {
                    "_id": data[0]["_id"],
                    "name": data[0]["name"],
                    "link_image": data[0]["link_image"],
                    "price": locale.format_string("%.0f", min(price), grouping=True)
                }
                datas.append(data_compare)
    categories = list(db.categories.find())
    return render_template("user/compare/index.html",category=g.categories,lists=datas,categories=categories)

@app.route('/home/product')
def home_product():
    query = {}
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
    per_page = 12
    skip = (page - 1) * per_page
    total = db.products.count_documents(query)
    lists = db.products.find(query)
    lists = list(lists.skip(skip).limit(per_page))
    for item in lists:
        item["store"] = db.stores.find_one({"_id": item["store_id"]})
        item["price"] = locale.format_string("%.0f", int(item["price"]), grouping=True)
    displayed_page_nums = Product().get_displayed_pages(page,int(ceil(total / per_page)),5)
    
    stores = list(db.stores.find())
    categories = list(db.categories.find())
    return render_template("user/product/index.html",category=g.categories,lists=lists,pages=displayed_page_nums,current_page=page,stores=stores,categories=categories)

def find_common_subarrays(string1, string2):
    word_array1 = string1.split()
    word_array2 = string2.split()
    common_subarrays = []

    for word1 in word_array1:
        if word1 in word_array2 and word1 not in common_subarrays:
            common_subarrays.append(word1)

    return common_subarrays


def find_longest_common_subarray(string, string_list):
    longest_subarray = []
    max_common_count = 0

    for s in string_list:
        common_subarrays = find_common_subarrays(string, s)
        common_count = len(common_subarrays)
        if common_count > max_common_count:
            max_common_count = common_count
            longest_subarray = common_subarrays

    return longest_subarray

def is_subarray_in_string(subarray, string):
    subarray_set = set(subarray)
    string_set = set(string.split())

    return subarray_set.issubset(string_set)

def calculate_similarity_percentage(string1, string2):
    matcher = difflib.SequenceMatcher(None, string1, string2)
    similarity_ratio = matcher.ratio()
    similarity_percentage = similarity_ratio * 100
    return similarity_percentage

@app.route('/home/product/compare/detail/<id>',methods=['GET'])
def product_compare_detail(id):
    product = db.products.find_one({"_id":id})
    name_product = product["name"].replace("(", "").replace(")", "").replace("Chính hãng","").replace("VN/A","").replace("-","").strip()
    datas = list(db.products.find({"category_id": product["category_id"],"store_id": {"$nin": [product["store_id"]]} }).distinct("name"))
    longest_substring = find_longest_common_subarray(name_product, datas)
    price = []
    list_data = []
    min_product = {}
    if longest_substring:
        datas = list(db.products.find({"category_id": product["category_id"]},{"name":1,"price":1,"store_id":1,"link_image":1,"updated_at":1}))
        for item in datas:
            item["price_int"] = item["price"]
            item["price"] = locale.format_string("%.0f", int(item["price"]), grouping=True)
            name = item["name"].replace("(", "").replace(")","")
            data = is_subarray_in_string(longest_substring,name)
            if data:
                item["store"] = db.stores.find_one({"_id": item["store_id"]},{"name":1,"link_image":1})
                ss1 = calculate_similarity_percentage(item["name"]," ".join(longest_substring))
                item["ss"] = ss1
                list_data.append(item)
                
        max_ss_dict = {}
        for data_dict in list_data:
            id_value = data_dict["store_id"]
            ss_value = data_dict["ss"]
            if id_value in max_ss_dict:
                if ss_value > max_ss_dict[id_value]:
                    max_ss_dict[id_value] = ss_value
            else:
                max_ss_dict[id_value] = ss_value

        result_list = []
        for data_dict in list_data:
            id_value = data_dict["store_id"]
            ss_value = data_dict["ss"]

            if ss_value == max_ss_dict[id_value]:
                result_list.append(data_dict)
                price.append(data_dict["price"])      
        for item in result_list:
            price_data = item["price"]
            if price_data == min(price):
                min_product = item
        result_list.remove(min_product)   
    else:
        min_product = product
        min_product["store"] = db.stores.find_one({"_id": min_product["store_id"]},{"name":1,"link_image":1})
    price = product["price"]
    similar_product = list(db.products.find({
        "category_id" : {"$nin": [product["category_id"]]},
        "price": {"$gte": price - 500000, "$lt": price + 500000}
    },{
        "_id":1,
        "name":1,
        "price":1,
        "link_image":1,
        "store_id":1
    }))
    for item in similar_product:
        item["store"] = db.stores.find_one({"_id": item["store_id"]})
        item["price"] = locale.format_string("%.0f", int(item["price"]), grouping=True)
    return render_template("user/compare/detail.html",min_product=min_product,list_data=result_list,similar_product=similar_product,category=g.categories)

@app.route('/home/product/compare/rating/<id>',methods=['GET'])
def product_compare_rating(id):
    product = db.products.find_one({"_id":id})
    name_product = product["name"].replace("(", "").replace(")", "").replace("Chính hãng","").replace("VN/A","").replace("-","").strip()
    datas = list(db.products.find({"category_id": product["category_id"],"store_id": {"$nin": [product["store_id"]]} }).distinct("name"))
    longest_substring = find_longest_common_subarray(name_product, datas)
    price = []
    rating = []
    list_data = []
    min_product = {}
    if longest_substring:
        datas = list(db.products.find({"category_id": product["category_id"]},{"name":1,"price":1,"store_id":1,"link_image":1}))
        for item in datas:
            item["price_int"] = item["price"]
            item["price"] = locale.format_string("%.0f", int(item["price"]), grouping=True)
            name = item["name"].replace("(", "").replace(")","")
            data = is_subarray_in_string(longest_substring,name)
            if data:
                item["store"] = db.stores.find_one({"_id": item["store_id"]},{"name":1,"link_image":1})
                item["rating"] = db.productdetails.find_one({"product_id": item["_id"]},{"rating":1,"total_rating":1})
                ss1 = calculate_similarity_percentage(item["name"]," ".join(longest_substring))
                item["ss"] = ss1
                if item["rating"] == None:
                    item["rating"] = {}
                    item["rating"]["rating"] = 0
                    item["rating"]["total_rating"] = 0
                list_data.append(item)
                
        max_ss_dict = {}
        for data_dict in list_data:
            id_value = data_dict["store_id"]
            ss_value = data_dict["ss"]
            if id_value in max_ss_dict:
                if ss_value > max_ss_dict[id_value]:
                    max_ss_dict[id_value] = ss_value
            else:
                max_ss_dict[id_value] = ss_value

        result_list = []
        for data_dict in list_data:
            id_value = data_dict["store_id"]
            ss_value = data_dict["ss"]

            if ss_value == max_ss_dict[id_value]:
                result_list.append(data_dict)
                rating_data = data_dict["rating"]["rating"]
                rating.append(rating_data)
      
        for item in result_list:
            price_data = float(item["rating"]["rating"])
            rating = [float(item) for item in rating if isinstance(item, (int, float)) or (isinstance(item, str) and item.replace(".", "", 1).isdigit())]
            if price_data == max(rating):
                min_product = item
        result_list.remove(min_product)  
    else:
        min_product = product
        min_product["store"] = db.stores.find_one({"_id": min_product["store_id"]},{"name":1,"link_image":1})
    price = product["price"]
    similar_product = list(db.products.find({
        "category_id" : {"$nin": [product["category_id"]]},
        "price": {"$gte": price - 500000, "$lt": price + 500000}
    },{
        "_id":1,
        "name":1,
        "price":1,
        "link_image":1,
        "store_id":1
    }))
    for item in similar_product:
        item["store"] = db.stores.find_one({"_id": item["store_id"]})
        item["price"] = locale.format_string("%.0f", int(item["price"]), grouping=True)
    return render_template("user/compare/rating.html",min_product=min_product,list_data=result_list,similar_product=similar_product,category=g.categories)

@app.route('/home/product/detail/<id>',methods=['GET'])
def product_detail(id):
    product = db.products.find_one({"_id":id})
    price = product["price"]
    category = db.categories.find_one({"_id": product["category_id"]},{"_id":1,"name":1,"parent_id":1})
    cate = []
    if category["parent_id"]:
        cate = list(db.categories.find({"parent_id": category["parent_id"]}).distinct('_id'))
    similar_product = list(db.products.find({
        'category_id': {'$in': cate},
        "price": {"$gte": price - 500000, "$lt": price + 500000}
    },{
        "_id":1,
        "name":1,
        "price":1,
        "link_image":1,
        "store_id":1
    }))
    for item in similar_product:
        item["store"] = db.stores.find_one({"_id": item["store_id"]})
        item["price"] = locale.format_string("%.0f", int(item["price"]), grouping=True)
    product["price"] = locale.format_string("%.0f", int(product["price"]), grouping=True)
    product["store"] = db.stores.find_one({"_id": product["store_id"]})
    productdetail = db.productdetails.find_one({"product_id": id})
    return render_template("user/product/detail.html",productdetail=productdetail,product=product,similar_product=similar_product,category=g.categories)