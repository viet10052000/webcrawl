from flask import Flask, jsonify, request, session, redirect
from app import db
import uuid
  
class Schedule:
    def create(self):
        schedule = {
            "_id": uuid.uuid4().hex,
            "name": request.values.get('name'),
            "crawlproduct_id": request.values.get('crawlproduct_id'),
            "last_execution_time": "",
            "next_execution_time": "",            
            "message": "",
            "status": "",
            "total": "",
            "updated_at": datetime.utcnow(),
            "created_at": datetime.utcnow()
        }
        schedule = db.schedules.insert_one(store)
        return schedule
    
    def index(self):
        schedules = list(db.schedules.find())
        return schedules
    
    def update(self, id, data):
        schedule = db.schedules.update_one({ '_id': id }, { '$set': data })
        
    def delete(self, id):
        schedule = db.schedules.find_one_and_delete({ '_id': id })
        return schedule