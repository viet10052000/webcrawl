from flask import Flask, jsonify, request, session, redirect
from app import db
import uuid
class CrawlProductDetail:
    def create(self, crawlproduct_id):
        crawl = {
            "_id": uuid.uuid4().hex,
            "selector_price": request.values.get('selector_price'),
            "selector_link_image": request.values.get('selector_link_image'),
            "selector_specification_frame": request.values.get('selector_specification_frame'),
            "selector_specification_name": request.values.get('selector_specification_name'),
            "selector_specification_detail": request.values.get('selector_specification_detail'),
            "selector_specification_button": request.values.get('selector_specification_button'),
            "selector_rating": request.values.get('selector_rating'),
            "selector_total_rating": request.values.get('selector_total_rating'),
            "selector_description": request.values.get('selector_description'),
            "crawlproduct_id": crawlproduct_id,
        }
        db.crawlproductdetails.insert_one(crawl)
    
    def index(self):
        lists = list(db.crawlproductdetails.find())
        return lists
    
    def update(self, id, data):
        db.crawlproductdetails.update_one({ '_id': id }, { '$set': data })
        
    def delete(self, id):
        crawlproductdetail = db.crawlproductdetails.find_one_and_delete({ '_id': id })
        return crawlproductdetail  
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
        }
        db.crawlproducts.insert_one(crawl)
        return crawl
    
    def index(self):
        lists = list(db.crawlproducts.find())
        return lists
    
    def update(self, id, data):
        db.crawlproducts.update_one({ '_id': id }, { '$set': data })
        
    def delete(self, id):
        crawlproduct = db.crawlproducts.find_one_and_delete({ '_id': id })
        return crawlproduct