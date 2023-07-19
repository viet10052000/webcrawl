from flask import Flask, jsonify, request, session, redirect
from app import db
import uuid
from passlib.hash import pbkdf2_sha256

class User:
    def create(self):
        user = {
            "_id": uuid.uuid4().hex,
            "firstname": request.values.get('firstname'),
            "lastname": request.values.get('lastname'),
            "gender": request.values.get('gender'),
            "birthday": request.values.get('birthday'),
            "email": request.values.get('email'),
            "password": request.values.get('password'),
            "role": request.values.get('role')
        }
        
        user['password'] = pbkdf2_sha256.encrypt(user['password'])
        
        if not user['email'] or not user['password'] or not user['firstname'] or not user['lastname'] or not user['gender'] or not user['birthday']:
            return 'Dữ liệu không được để trống'
        if db.users.find_one({ "email": user['email'] }):
            return 'Email đã tồn tại'
        if db.users.insert_one(user):
            return 'success'
            
    def index(self):
        users = list(db.users.find())
        return users
    
    def update(self):
        id = session['user']['_id']
        user = {
            "_id": id,
            "name": request.values.get('name'),
            "email": request.values.get('email'),
            "role": request.values.get('role')
        }
        user = db.users.update_one({ '_id': id }, { '$set': data })
        
    def delete(self, id):
        user = db.users.find_one_and_delete({ '_id': id })
        return user