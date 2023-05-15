from flask import Flask, session, render_template, redirect
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from functools import wraps
app = Flask(__name__)
app.secret_key = b"\x8d\x17Jw\x02\xcbY\xb8\xdb8\xe7\x02\xd4'\xef\xf0"
uri = 'mongodb+srv://user:123456Aa@cluster0.t3aqomt.mongodb.net'
# database
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
db = client.shops
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
from user import routes
from webcrawl import routes
from toolcrawl import routes
from shop import routes
from category import routes
from product import routes
if __name__ == '__main__':
    app.run(debug = True)