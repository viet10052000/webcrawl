from flask import Flask, jsonify, request, session, redirect
from app import db
import uuid

class Category:
    def create(self):
        category = {
            "_id": uuid.uuid4().hex,
            "name": request.values.get('name'),
            "description": request.values.get('description'),
            "parent_id": request.values.get('parent_id'),
        }
        category = db.categories.insert_one(category)
        return category
    
    def index(self):
        categories = list(db.categories.find())
        return categories
    
    def update(self, id, data):
        category = db.categories.update_one({ '_id': id }, { '$set': data })
        
    def delete(self, id):
        category = db.categories.find_one_and_delete({ '_id': id })
        return category