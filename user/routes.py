from flask import Flask, render_template, request, redirect, jsonify, session
from app import app, login_required, roles_required, db
from passlib.hash import pbkdf2_sha256
from user.models import User

@app.route('/user/list')
@login_required
@roles_required('admin')
def userlist():
    lists = User().index()
    return render_template('admin/user/list.html',lists=lists)

@app.route('/user/create', methods=['GET','POST'])
@login_required
@roles_required('admin')
def usercreate():
    if request.method == 'GET':
        users = list(db.users.find())
        return render_template('admin/user/create.html',users=users)
    elif request.method == 'POST':
        data = User().create()
        return redirect('/user/list')
    
    
@app.route('/user/delete/<id>', methods=['GET'])
@login_required
@roles_required('admin')
def userdelete(id):
    lists = User().delete(id)
    return redirect('/user/list')

@app.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('admin/profile.html')

@app.route('/profile/edit', methods=['GET','POST'])
@login_required
def profileEdit():
    if request.method == 'GET':
        user = db.users.find_one({'_id': session['user']['_id']})
        return render_template('admin/user/edit.html',user=user)
    elif request.method == 'POST':
        user = db.users.find_one({'_id': session['user']['_id']})
        data = {
            '_id': user['_id'],
            'name': request.values.get('name'),
            'email': request.values.get('email'),
            'password': user['password'],
            'isAdmin': user['isAdmin'],
        }
        db.users.update_one({ '_id': user['_id'] }, { '$set': data })
        return redirect('/profile')
    
@app.route('/changepassword', methods=['GET','POST'])
@login_required
def changePassword():
    if request.method == 'GET':
        user = db.users.find_one({'_id': session['user']['_id']})
        return render_template('admin/user/changepass.html',user=user)
    elif request.method == 'POST':
        user = db.users.find_one({'_id': session['user']['_id'],'password': pbkdf2_sha256.encrypt(request.values.get('old_password'))})
        data = {
            '_id': user['_id'],
            'name': request.values.get('name'),
            'email': request.values.get('email'),
            'password': user['password'],
            'isAdmin': user['isAdmin'],
        }
        db.users.update_one({ '_id': user['_id'] }, { '$set': data })
        return redirect('/profile')
    