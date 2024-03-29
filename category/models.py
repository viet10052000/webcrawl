from flask import Flask, jsonify, request, session, redirect
from app import db
import uuid, base64
from bson.binary import Binary
class Category:
    def create(self):
        image = request.files['image']
        if image:
            image_data = image.read()
            binary_data = Binary(image_data)
        else:
            binary_data = ''
        category = {
            "_id": uuid.uuid4().hex,
            "name": request.values.get('name'),
            "image": binary_data,
            "description": request.values.get('description'),
            "parent_id": request.values.get('parent_id'),
        }
        if not request.values.get('name'):
            return 'Tên không được để trống.'
        if not image:
            return 'Ảnh không được để trống.'
        if db.categories.find_one({'name': category['name'] }):
            return 'Tên danh mục đã tồn tại.'
        if db.categories.insert_one(category):
            return 'success'
        return 'Thêm danh mục không thành công'
    
    def index(self):
        lists = list(db.categories.find())
        for item in lists:
            if "image" in item:
                try:
                    image_base64 = base64.b64decode(item['image']["$binary"]["base64"])
                    encoded_image_base64 = base64.b64encode(image_base64).decode('ascii')
                    item["image"] = encoded_image_base64
                except:
                    image_base64 = base64.b64encode(item['image']).decode('ascii')
                    item["image"] = image_base64
        return lists
    
    def update(self, id, data):
        category = db.categories.find_one({'_id': id })
        if not request.values.get('name'):
            return 'Tên không được để trống.'
        if not data["image"]:
            return 'Ảnh không được để trống.'
        if db.categories.find_one({'name': data['name'] }) and category["name"] != data["name"]:
            return 'Tên danh mục đã tồn tại.'
        if db.categories.update_one({ '_id': id }, { '$set': data }):
            return 'success'
        return 'Sửa danh mục không thành công'
        
    def delete(self, id):
        category = db.categories.find_one_and_delete({ '_id': id })
        return category
    
    def get_displayed_pages(self, current_page, num_pages, max_displayed_pages=5):
        half_max_displayed = max_displayed_pages // 2
        if num_pages <= max_displayed_pages:
            return list(range(1, num_pages+1))
        elif current_page - half_max_displayed <= 1:
            return list(range(1, max_displayed_pages+1)) + ["...", num_pages]
        elif current_page + half_max_displayed >= num_pages:
            return [1, "..."] + list(range(num_pages-max_displayed_pages+2, num_pages+1))
        else:
            return [1, "..."] + list(range(current_page-half_max_displayed, current_page+half_max_displayed+1)) + ["...", num_pages]