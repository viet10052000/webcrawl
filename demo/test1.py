def build_failure_table(pattern):
    m = len(pattern)
    failure = [0] * m
    j = 0

    for i in range(1, m):
        if pattern[i] == pattern[j]:
            j += 1
            failure[i] = j
        else:
            if j != 0:
                j = failure[j - 1]
                i -= 1
            else:
                failure[i] = 0

    return failure


def longest_common_substring(str1, str2):
    n = len(str1)
    m = len(str2)
    failure = build_failure_table(str2)
    i = 0
    j = 0
    longest = ""

    while i < n:
        if str1[i] == str2[j]:
            i += 1
            j += 1
            if j == m:
                longest = str2
                break
        else:
            if j != 0:
                j = failure[j - 1]
            else:
                i += 1

    return longest


def find_longest_substring(string, strings):
    longest_substring = ""
    max_length = 0

    for s in strings:
        # print(s)
        substring = longest_common_substring(string, s)
        print(substring)
        if len(substring) > max_length:
            max_length = len(substring)
            longest_substring = substring
            # print(longest_substring)

    return longest_substring

import pymongo
import re
client = pymongo.MongoClient('mongodb+srv://user:123456Aa@cluster0.t3aqomt.mongodb.net')
db = client['shops']
category = db.categories.find_one({"name": 'macboook'})

iphone = "Apple MacBook Air M1 256GB 2020 I Chính hãng Apple Việt Nam".replace("(", "").replace(")", "")
store_id = "4883128f5159462fa63340991805885b"
print(iphone)
datas = list(db.products.find({"category_id": category["_id"],"store_id": {"$nin": [store_id]} }).distinct("name"))
# print(datas)
longest_string = find_longest_substring(iphone,datas)
print("longest_string: ",longest_string)
datas = list(db.products.find({"category_id": category["_id"],"store_id": {"$nin": [store_id]}},{"name":1,"price":1,"store_id":1}))
price = []
list_data = []
for item in datas:
  name = item["name"].replace("(", "").replace(")","")
  if longest_string in name:
    list_data.append(item)
    price.append(item["price"])
  del item["store_id"]
# print(list_data)
group = {
  "name" : longest_string,
  "min_price" : min(price),
  "max_price" : max(price)
}
print(group)
# list_store = list(db.products.find({},{"store_id":1}).distinct("store_id"))
# for item in list_store:
#     datas = list(db.products.find({"category_id": category["_id"]}).distinct("name"))
#     longest_string = find_longest_string(iphone,datas)
#     datas = list(db.products.find({"category_id": category["_id"]},{"name":1,"price":1,"store_id":1}))
#     price = []
#     list_data = []
#     for item in datas:
#         name = item["name"].replace("(", "").replace(")","")
#         item["store_name"] = db.stores.find_one({"_id":item["store_id"]})["name"]
#         if longest_string in name:
#             list_data.append(item)
#             price.append(item["price"])
#         del item["store_id"]
#     group = {
#     "name" : longest_string,
#     "min_price" : min(price),
#     "max_price" : max(price)
#     }
#     print(group)