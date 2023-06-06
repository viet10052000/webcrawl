import difflib
import pymongo

# Kết nối tới MongoDB
client = pymongo.MongoClient('mongodb+srv://user:123456Aa@cluster0.t3aqomt.mongodb.net')
db = client['shops']
collection = db['products']
categories = db['categories']
# Dữ liệu ban đầu
import re
products = list(collection.find())
categories = list(db.categories.find({},{'_id':1,'name':1}))
print(categories)