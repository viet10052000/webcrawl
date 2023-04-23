from flask import Flask, jsonify, request, session, redirect
from app import db
import uuid

class Store:
    def create(self):
        store = {
            "_id": uuid.uuid4().hex,
            "name": request.values.get('name'),
            "link_image": request.values.get('link_image'),
            "link_url": request.values.get('link_url')
        }
        if db.stores.find_one({'name': store['name'] }):
            return jsonify({'error' : 'Tên cửa hàng đã tồn tại'}), 400
        if db.stores.find_one({'link_url': store['link_url'] }):
            return jsonify({'error' : 'Đường dẫn cửa hàng đã tồn tại'}), 400
        store = db.stores.insert_one(store)
        return store
    
    def index(self):
        stores = list(db.stores.find())
        return stores
    
    def update(self, id, data):
        store = db.stores.update_one({ '_id': id }, { '$set': data })
        
    def delete(self, id):
        store = db.stores.find_one_and_delete({ '_id': id })
        return store