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
        if not request.values.get('name') or not request.values.get('link_image') or not request.values.get('link_url'):
            return 'Dữ liệu không được để trống'
        if db.stores.find_one({'name': store['name'] }):
            return 'Tên cửa hàng đã tồn tại'
        if db.stores.find_one({'link_url': store['link_url'] }):
            return 'Đường dẫn cửa hàng đã tồn tại'
        if db.stores.insert_one(store):
            return 'success'
    
    def index(self):
        stores = list(db.stores.find())
        return stores
    
    def update(self, id, data):
        store = db.stores.find_one({ '_id' : id })
        if not data['name'] or not data['link_image'] or not data['link_url']:
            return 'Dữ liệu không được để trống.'
        if db.stores.find_one({'name': data['name'] }) and store["name"] != data["name"]:
            return 'Tên cửa hàng đã tồn tại.'
        if db.stores.find_one({'link_url': data['link_url'] }) and store["link_url"] != data["link_url"]:
            return 'Đường dẫn cửa hàng đã tồn tại.'
        if db.stores.update_one({ '_id': id }, { '$set': data }):
            return 'success'
        return 'Sửa cửa hàng không thành công.'
        
    def delete(self, id):
        store = db.stores.find_one_and_delete({ '_id': id })
        return store