import difflib
import pymongo

# Kết nối tới MongoDB
client = pymongo.MongoClient('mongodb+srv://user:123456Aa@cluster0.t3aqomt.mongodb.net')
db = client['shops']
collection = db['products']
# Dữ liệu ban đầu
import re
products = list(collection.find({"price": ""}))
for item in products:
  collection.update_one({"price": ""}, {'$set': {'price': 0}})


# keyword = "iphone"

# # Sử dụng biểu thức chính quy để tìm kiếm theo từ khóa
# regex = re.compile(keyword, re.IGNORECASE)
# query = {"name": {"$regex": regex}}
# data = list(collection.find(query))
# print(data)
# datas = []
# for item in data:
#   datas.append(item["name"])
# # # Gom dữ liệu theo tên gần giống
# clusters = []

# for item in datas:
#     # Kiểm tra xem item có thuộc vào một cluster hiện có hay không
#     is_added = False
    
#     for cluster in clusters:
#         for cluster_item in cluster:
#             similarity = difflib.SequenceMatcher(None, item, cluster_item).ratio()
            
#             # Nếu độ tương đồng lớn hơn ngưỡng, thêm item vào cluster
#             if similarity >= 0.8:
#                 cluster.append(item)
#                 is_added = True
#                 break
        
#         if is_added:
#             break
    
#     # Nếu item không thuộc vào bất kỳ cluster nào, tạo một cluster mới chứa item
#     if not is_added:
#         clusters.append([item])

# # In ra kết quả
# for cluster in clusters:
#     print(cluster)
