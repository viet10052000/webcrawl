from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask, session, render_template, redirect, g
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from functools import wraps
from dotenv import load_dotenv
import os, re, json, base64
import uuid
from apscheduler.schedulers.background import BackgroundScheduler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time, math
app = Flask(__name__)
load_dotenv()
app.secret_key = b"\x8d\x17Jw\x02\xcbY\xb8\xdb8\xe7\x02\xd4'\xef\xf0"
# database
# Create a new client and connect to the server
client = MongoClient(os.getenv('MONGODB_URI'), server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
db = client[os.getenv('DATABASE_NAME')]
scheduler = BackgroundScheduler(daemon=True)
# routes
from auth import routes
#decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logger_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/login')
    
    return wrap

@app.errorhandler(404)
def page_not_found(e):
    return render_template('/adminv2/error/404.html'), 404

def roles_required(*role_names):
    def decorator(original_route):
        @wraps(original_route)
        def decorated_route(*args, **kwargs):          
            if not session['user']['role'] in role_names:
                return render_template('/adminv2/error/403.html')
            else:
                return original_route(*args, **kwargs)
        return decorated_route
    return decorator

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.client.close()

def fetch_categories_from_db():
    categories = list(db.categories.find())
    cate = []
    category = []
    for item in categories:
        if not item["parent_id"]:
            cate.append(item)
    for ca in cate:
        child = list(db.categories.find({"parent_id": ca["_id"]}))
        for i in child:
            try:
                image_base64 = base64.b64decode(i['image']["$binary"]["base64"])
                encoded_image_base64 = base64.b64encode(image_base64).decode('ascii')
                i["image"] = encoded_image_base64
            except:
                image_base64 = base64.b64encode(i['image']).decode('ascii')
                i["image"] = image_base64

        category_item = {
            "_id": ca["_id"],
            "name": ca["name"],
            "image": ca["image"],
            "child": child
        }
        category.append(category_item)
    return category

@app.before_request
def before_request():
    g.categories = fetch_categories_from_db()

from user import routes
from webcrawl import routes
from toolcrawl import routes
from shop import routes
from category import routes
from product import routes
from schedule import routes
from demo import job

if __name__ == '__main__':
    app.run(debug=True)