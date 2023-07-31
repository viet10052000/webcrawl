from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
from datetime import datetime, timedelta
# database
# Create a new client and connect to the server
client = MongoClient('mongodb+srv://user:123456Aa@cluster0.t3aqomt.mongodb.net', server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
db = client['shops']
stores = list(db.products.find({"store_id":"9247580264714d23afcbd1c6ab5894c5","category_id": "109fe83691614079b53722577078a70a"}))
for item in stores:
  db.products.delete_one({"_id": item["_id"]})
# for item in stores:
#   print(item)
#   pricehistory = [
#     {
#       "price": item["price"],
#       "created_at": datetime.now()
#     },
#     {
#       "price": item["price"],
#       "created_at": datetime.now() - timedelta(days=1)
#     },
#     {
#       "price": item["price"],
#       "created_at": datetime.now() - timedelta(days=2)
#     },
#     {
#       "price": item["price"],
#       "created_at": datetime.now() - timedelta(days=3)
#     },
#     {
#       "price": item["price"],
#       "created_at": datetime.now() - timedelta(days=4)
#     },
#     {
#       "price": item["price"],
#       "created_at": datetime.now() - timedelta(days=5)
#     },
#     {
#       "price": item["price"],
#       "created_at": datetime.now() - timedelta(days=6)
#     }
#   ]
#   db.products.update_one({'_id': item["_id"]},{
#     "$set" : {
#       "price_history": pricehistory,
#       "updated_at" : datetime.now(),
#       "created_at" : datetime.now()
#     }
#   })