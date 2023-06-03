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
        category = db.categories.insert_one(category)
        return category
    
    def index(self):
        lists = list(db.categories.find())
        for item in lists:
            if "image" in item:
                image_base64 = base64.b64encode(item['image']).decode('utf-8')
                item["image"] = image_base64
        return lists
    
    def update(self, id, data):
        category = db.categories.update_one({ '_id': id }, { '$set': data })
        
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