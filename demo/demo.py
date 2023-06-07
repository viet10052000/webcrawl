import difflib
import pymongo

# Kết nối tới MongoDB
client = pymongo.MongoClient('mongodb+srv://user:123456Aa@cluster0.t3aqomt.mongodb.net')
db = client['shops']

categories = db.categories.find_one({"name": "iphone"},{'_id':1,'name':1})
products = list(db.products.find({"category_id": categories["_id"]},{"name":1}))
list_ip = []
for item in products:
  list_ip.append(item["name"])

iphone_list = [
    "iPhone 14 Pro Max 128GB",
    "iPhone 14 Pro Max 512GB",
    "iPhone 14 Pro Max 256GB",
    "iPhone 14 Pro 128GB",
    "iPhone 14 Pro 256GB",
    "iPhone 14 Pro 512GB",
    "iPhone 14 128GB",
    "iPhone 14 256GB",
    "iPhone 14 Plus 128GB",
    "iPhone 14 Plus 256GB",
    "iPhone 14 Plus 512GB",
    "iPhone 13 128GB",
    "iPhone 12 64GB",
    "iPhone 12 128GB",
    "iPhone 11 64GB",
    "iPhone 11 128GB",
    "iPhone SE (2022) 128GB",
    "iPhone SE (2022) 64GB"
]

grouped_iphones = {}

for iphone in iphone_list:
    name = " ".join(iphone.split()[:-1])  # Lấy tên iPhone bằng cách loại bỏ thông tin về dung lượng
    if name in grouped_iphones:
        grouped_iphones[name].append(iphone)
    else:
        grouped_iphones[name] = [iphone]

# # In kết quả
# for name, models in grouped_iphones.items():
#     print(name + ":")
#     for model in models:
#         print("  - " + model)
