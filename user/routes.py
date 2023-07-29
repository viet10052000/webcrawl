from flask import Flask, render_template, request, redirect, jsonify, session, g, flash
from app import app, login_required, roles_required, db
from passlib.hash import pbkdf2_sha256
from user.models import User
from auth.models import Auth
@app.route('/user/list')
@login_required
@roles_required('admin')
def userlist():
    lists = User().index()
    return render_template('adminv2/user/list.html',lists=lists)

@app.route('/user/create', methods=['GET','POST'])
@login_required
@roles_required('admin')
def usercreate():
    if request.method == 'GET':
        return render_template('adminv2/user/create.html')
    elif request.method == 'POST':
        data = User().create()
        if 'success' in data:
            flash('Thêm người dùng thành công!')
            return redirect('/user/list')
        flash(data)
        return redirect('/user/create')
    
@app.route('/user/delete/<id>', methods=['GET'])
@login_required
@roles_required('admin')
def userdelete(id):
    lists = User().delete(id)
    flash('Xóa người dùng thành công!')
    return redirect('/user/list')

@app.route('/profile/admin', methods=['GET'])
@login_required
@roles_required('admin','collector')
def profile_admin():
    user = db.users.find_one({'_id': session['user']['_id']})
    return render_template('adminv2/user/profile.html',user=user)

@app.route('/profile', methods=['GET'])
@login_required
def profile():
    user = db.users.find_one({'_id': session['user']['_id']})
    return render_template('user/auth/myprofile.html',user=user,category=g.categories)

@app.route('/profile/edit', methods=['GET','POST'])
@login_required
def profileEdit():
    if request.method == 'GET':
        user = db.users.find_one({'_id': session['user']['_id']})
        return render_template('user/auth/editprofile.html',user=user,category=g.categories)
    elif request.method == 'POST':
        user = User().find(session['user']['_id'])
        data = {
            "firstname": request.values.get('firstname'),
            "lastname": request.values.get('lastname'),
            "gender": request.values.get('gender'),
            "birthday": request.values.get('birthday'),
        }
        user = User().update(user['_id'], data)
        return redirect('/profile')

@app.route('/changepassword/admin', methods=['GET','POST'])
@login_required
@roles_required('admin','collector')
def changePassword_admin():
    if request.method == 'GET':
        return render_template('adminv2/user/changepass.html',category=g.categories)
    elif request.method == 'POST':
        user = db.users.find_one({'_id': session['user']['_id']})
        checkpass = pbkdf2_sha256.verify(request.values.get('old_password'), user['password'])
        if checkpass == False:
            data = {
                "error":"Mật khẩu không chính xác"
            }
            return render_template('adminv2/user/changepass.html',user=data)
        else:
            if request.values.get('old_password') == request.values.get('new_password'):
                data = {
                    "error":"Mật khẩu không được trùng"
                }
                return render_template('adminv2/user/changepass.html',user=data)
            elif request.values.get('new_password') != request.values.get('confirm_password'):
                data = {
                    "error":"Mật khẩu xác nhận không chính xác"
                }
                return render_template('adminv2/user/changepass.html',user=data) 
            else:
                data = {
                    'old_password': request.values.get('old_password'),
                    'new_password': request.values.get('new_password'),
                    'confirm_password': request.values.get('confirm_password'),
                }
                password = pbkdf2_sha256.encrypt(data['new_password'])
                user["password"] = password
                db.users.update_one({ '_id': user['_id'] }, { '$set': user })
                Auth().signout()
                return redirect('/login')
    
@app.route('/changepassword', methods=['GET','POST'])
@login_required
def changePassword():
    if request.method == 'GET':
        return render_template('user/auth/changepassword.html',category=g.categories)
    elif request.method == 'POST':
        user = db.users.find_one({'_id': session['user']['_id']})
        checkpass = pbkdf2_sha256.verify(request.values.get('old_password'), user['password'])
        if checkpass == False:
            data = {
                "error":"Mật khẩu không chính xác"
            }
            return render_template('user/auth/changepassword.html',user=data)
        else:
            if request.values.get('old_password') == request.values.get('new_password'):
                data = {
                    "error":"Mật khẩu không được trùng"
                }
                return render_template('user/auth/changepassword.html',user=data)
            elif request.values.get('new_password') != request.values.get('confirm_password'):
                data = {
                    "error":"Mật khẩu xác nhận không chính xác"
                }
                return render_template('user/auth/changepassword.html',user=data) 
            else:
                data = {
                    'old_password': request.values.get('old_password'),
                    'new_password': request.values.get('new_password'),
                    'confirm_password': request.values.get('confirm_password'),
                }
                password = pbkdf2_sha256.encrypt(data['new_password'])
                user["password"] = password
                db.users.update_one({ '_id': user['_id'] }, { '$set': user })
                Auth().signout()
                return redirect('/login')
