from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db
import uuid
class Auth:
    
    def start_session(self, user):
        del user['password']
        session['logger_in'] = True
        session['user'] = user
        return jsonify(user), 200
    
    def sinup(self):
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.values.get('name'),
            "email": request.values.get('email'),
            "password": request.values.get('password'),
            "isAdmin": "0"
        }
        
        user['password'] = pbkdf2_sha256.encrypt(user['password'])
        
        if db.users.find_one({ "email": user['email'] }):
            return jsonify({ "error": "Email address already in use" }), 400
        
        if db.users.insert_one(user):
            return self.start_session(user)
        
        return jsonify({ "error": "Sign up failed" }), 400

    def signout(self):
        session.clear()
        return redirect('/')
    
    def login(self):
        user = db.users.find_one({
            "email": request.values.get('email')
        })
        
        if user and pbkdf2_sha256.verify(request.values.get('password'), user['password']):
            return self.start_session(user)
        
        return jsonify({ "error": "Invalid login creadentials"}), 401
        