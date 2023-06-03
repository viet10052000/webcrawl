from flask import Flask, jsonify, request, session, redirect
from app import db
import uuid
import datetime
class Schedule:
    def create(self):
        schedule = {
            "_id": uuid.uuid4().hex,
            "crawlproduct_id": request.values.get('crawlproduct_id'),       
            "message": "",
            "status": "",
            "total": "",
            "time_crawl_start": "",
            "time_repeat": "",
            "updated_at": datetime.utcnow(),
            "created_at": datetime.utcnow()
        }
        schedule = db.schedules.insert_one(schedule)
        return schedule
    
    def index(self):
        schedules = list(db.schedules.find())
        if schedules:
            return schedules
        else:
            return []
    
    def update(self, id, data):
        schedule = db.schedules.update_one({ '_id': id }, { '$set': data })
        
    def delete(self, id):
        schedule = db.schedules.find_one_and_delete({ '_id': id })
        return schedule