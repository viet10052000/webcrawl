from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
import re
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
stores = list(db.productdetails.find({},{"rating":1,"total_rating":1}))
for item in stores:
  if isinstance(item["rating"], str):
    if "/" in item["rating"]:
      item["rating"] = item["rating"].split("/")[0]
    item["rating"] = float(item["rating"])
  if isinstance(item["total_rating"], str):
    numbers = re.findall(r'\d+', item["total_rating"])
    if numbers:
      item["total_rating"] = int(numbers[0])
    else:
      item["total_rating"] = 0
  print(item["rating"])
  print(item["total_rating"])
  db.productdetails.update_one({"_id": item["_id"]},{"$set": { 
    "rating": item["rating"],
    "total_rating": item["total_rating"]  
  }})