from flask import Flask, render_template, request, redirect, jsonify
from app import app
from auth.models import Auth

@app.route('/register', methods=['GET','POST'])
def signup():
    if request.method == 'GET':    
        return render_template('user/auth/register.html')
    elif request.method == 'POST':
        user = Auth().sinup()
        if "error" in user:
            return render_template('user/auth/register.html',user=user)
        else:
            return redirect('/login')  

@app.route('/signout')
def signout():
    return Auth().signout()

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':    
        return render_template('user/auth/login.html')
    elif request.method == 'POST':
        user = Auth().login()
        if "error" in user:
            return render_template('user/auth/login.html',user=user)
        else:
            return redirect('/')  

    
  