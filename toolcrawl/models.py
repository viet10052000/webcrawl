from flask import Flask, jsonify, request, session, redirect
from app import db
import uuid
class CrawlProduct:
    def create(self):
        crawl = {
            "_id": uuid.uuid4().hex,
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
        db.crawlproducts.insert_one(crawl)
        return jsonify(crawl)
    
    def index(self):
        lists = list(db.crawlproducts.find())
        return lists
    
    def update(self, id, data):
        db.crawlproducts.update_one({ '_id': id }, { '$set': data })
        
    def delete(self, id):
        crawlproduct = db.crawlproducts.find_one_and_delete({ '_id': id })
        return crawlproduct