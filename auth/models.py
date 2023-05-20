from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db
import uuid
class Auth:
    
    def start_session(self, user):
        del user['password']
        session['logger_in'] = True
        session['user'] = user
        return user
    
    def sinup(self):
        user = {
            "_id": uuid.uuid4().hex,
            "firstname": request.values.get('firstname'),
            "lastname": request.values.get('lastname'),
            "gender": request.values.get('gender'),
            "birthday": request.values.get('birthday'),
            "email": request.values.get('email'),
            "password": request.values.get('password'),
            "role": "user"
        }
        
        user['password'] = pbkdf2_sha256.encrypt(user['password'])
        
        if db.users.find_one({ "email": user['email'] }):
            data = {
                "error": "Email đã tồn tại."
            }            
            return data
        
        if db.users.insert_one(user):
            return { "success" : "Đăng Ký Thành Công" }

    def signout(self):
        session.clear()
        return redirect('/')
    
    def login(self):
        user = db.users.find_one({
            "email": request.values.get('email')
        })
        
        if user and pbkdf2_sha256.verify(request.values.get('password'), user['password']):
            self.start_session(user)
            return { "success" : "Đăng Nhập Thành Công" }

        data = {
            "error": "Tên tài thoản hoặc mật khẩu không chính xác"
        }
        return data
        