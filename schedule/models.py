from flask import Flask, jsonify, request, session, redirect
from app import db
import uuid
from datetime import datetime
from dateutil.parser import isoparse
class Schedule:
    def create(self):
        if not request.values.get('time_repeat'):
            return 'Nhập khoảng cách ngày thu thập'
        schedule = {
            "_id": uuid.uuid4().hex,
            "crawlproduct_id": request.values.get('crawlproduct_id'),       
            "message": "",
            "status": False,
            "total": 0,
            "time_repeat": int(request.values.get('time_repeat')),
            "updated_at": datetime.now(),
            "created_at": datetime.now()
        }
        if db.schedules.find_one({'crawlproduct_id': schedule['crawlproduct_id'] }):
            return 'Trình thu thập tự động đã tồn tại'
        if db.schedules.insert_one(schedule):
            return 'success'
    
    def index(self):
        schedules = list(db.schedules.find())
        if schedules:
            return schedules
        else:
            return []
    
    def update(self, id, data):
        schedule = db.schedules.find_one({'_id': id })
        if not data['time_repeat']:
            return 'Nhập khoảng cách ngày thu thập'
        data['time_repeat'] = int(data['time_repeat'])
        if db.schedules.find_one({'crawlproduct_id': schedule['crawlproduct_id'] }) and data["crawlproduct_id"] != schedule['crawlproduct_id']:
            return 'Trình thu thập tự động đã tồn tại'
        if db.schedules.update_one({ '_id': id }, { '$set': data }):
            return 'success'
        
    def delete(self, id):
        schedule = db.schedules.find_one_and_delete({ '_id': id })
        return schedule