from flask import Flask, jsonify, request, session, redirect
from app import db
import uuid
from passlib.hash import pbkdf2_sha256

class User:
    def create(self):
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.values.get('name'),
            "email": request.values.get('email'),
            "password": request.values.get('password'),
            "role": request.values.get('is_admin')
        }
        
        user['password'] = pbkdf2_sha256.encrypt(user['password'])
        
        if db.users.find_one({ "email": user['email'] }):
            return jsonify({ "error": "Email address already in use" }), 400
        db.users.insert_one(user)
        return user
            
    def index(self):
        users = list(db.users.find())
        return users
    
    def update(self):
        id = session['user']['_id']
        user = {
            "_id": id,
            "name": request.values.get('name'),
            "email": request.values.get('email'),
            "role": request.values.get('is_admin')
        }
        user = db.users.update_one({ '_id': id }, { '$set': data })
        
    def delete(self, id):
        user = db.users.find_one_and_delete({ '_id': id })
        return user