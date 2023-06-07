from flask import Flask, jsonify, request, session, redirect
from app import db
import uuid
from schedule.models import Schedule
from datetime import datetime
from dateutil.parser import isoparse
class CrawlProductDetail:
    def create(self, crawlproduct_id):
        crawl = {
            "_id": uuid.uuid4().hex,
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
        if('check' in request.form):
            crawlproduct = db.crawlproducts.find_one({'store_id': request.values.get('store_id')})
            crawlproductdetail = db.crawlproductdetails.find_one({'crawlproduct_id': crawlproduct['_id']})
            crawl = {
                "_id": uuid.uuid4().hex,
                "name": request.values.get('name'),
                "category_id": request.values.get('category_id'),
                "store_id": request.values.get('store_id'),
                "link_url": request.values.get('link'),
                "selector_frame": crawlproduct['selector_frame'],
                "selector_name": crawlproduct['selector_name'],
                "selector_url": crawlproduct['selector_url'],
                "selector_price": crawlproduct['selector_price'],
                "selector_link_image": crawlproduct['selector_link_image'],
                "selector_load_page": crawlproduct['selector_load_page'],
            }
            crawlproductdetail = {
                "_id": uuid.uuid4().hex,
                "selector_specification_frame": crawlproductdetail['selector_specification_frame'],
                "selector_specification_name": crawlproductdetail['selector_specification_name'],
                "selector_specification_detail": crawlproductdetail['selector_specification_detail'],
                "selector_specification_button": crawlproductdetail['selector_specification_button'],
                "selector_rating": crawlproductdetail['selector_rating'],
                "selector_total_rating": crawlproductdetail['selector_total_rating'],
                "selector_description": crawlproductdetail['selector_description'],
                "crawlproduct_id": crawl['_id'],
            }
            db.crawlproducts.insert_one(crawl)
            db.crawlproductdetails.insert_one(crawlproductdetail)
        else:
            crawl = {
                "_id": uuid.uuid4().hex,
                "name": request.values.get('name'),
                "category_id": request.values.get('category_id'),
                "store_id": request.values.get('store_id'),
                "link_url": request.values.get('link'),
                "selector_frame": request.values.get('selector_frame'),
                "selector_name": request.values.get('selector_name'),
                "selector_url": request.values.get('selector_url'),
                "selector_price": request.values.get('selector_price'),
                "selector_link_image": request.values.get('selector_link_image'),
                "selector_load_page": request.values.get('selector_load_page'),
            }
            db.crawlproducts.insert_one(crawl)
            db.crawlproductdetails.insert_one(crawlproductdetail)
        if 'checkjobtimer' in request.form:
            schedule = {
                "_id": uuid.uuid4().hex,
                "crawlproduct_id": crawl['_id'],       
                "message": "",
                "status": False,
                "total": 0,
                "time_repeat": int(request.values.get('time_repeat')),
                "updated_at": datetime.now(),
                "created_at": datetime.now()
            }
            schedule = db.schedules.insert_one(schedule)
        return crawl
    
    def index(self):
        lists = list(db.crawlproducts.find())
        return lists
    
    def update(self, id, data):
        db.crawlproducts.update_one({ '_id': id }, { '$set': data })
        
    def delete(self, id):
        crawlproduct = db.crawlproducts.find_one_and_delete({ '_id': id })
        return 
    
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