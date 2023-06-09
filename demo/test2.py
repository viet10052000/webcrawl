def find_common_subarrays(string1, string2):
    word_array1 = string1.split()
    word_array2 = string2.split()
    common_subarrays = []

    for word1 in word_array1:
        if word1 in word_array2 and word1 not in common_subarrays:
            common_subarrays.append(word1)

    return common_subarrays


def find_longest_common_subarray(string, string_list):
    longest_subarray = []
    max_common_count = 0

    for s in string_list:
        common_subarrays = find_common_subarrays(string, s)
        common_count = len(common_subarrays)
        if common_count > max_common_count:
            max_common_count = common_count
            longest_subarray = common_subarrays

    return longest_subarray

import pymongo
import re
client = pymongo.MongoClient('mongodb+srv://user:123456Aa@cluster0.t3aqomt.mongodb.net')
db = client['shops']
category = db.categories.find_one({"name": 'iphone'})

iphone = "iPhone 14 Pro Max 128GB | Chính hãng VN/A".replace("|", "").replace("(", "").replace(")", "").replace("Chính hãng","").replace("VN/A","").strip()
store_id = "4883128f5159462fa63340991805885b"
print(iphone)
datas = list(db.products.find({"category_id": category["_id"],"store_id": {"$nin": [store_id]} }).distinct("name"))
longest_substring = find_longest_common_subarray(iphone, datas)
print("Longest common substring:", longest_substring)
datas = list(db.products.find({"category_id": category["_id"]},{"name":1,"price":1,"store_id":1}))
price = []
list_data = []
def is_subarray_in_string(subarray, string):
    subarray_set = set(subarray)
    string_set = set(string.split())

    return subarray_set.issubset(string_set)
for item in datas:
  name = item["name"].replace("(", "").replace(")","")
  data = is_subarray_in_string(longest_substring,name)
  if data:
    list_data.append(item)
    price.append(item["price"])
  del item["store_id"]
print(list_data)
group = {
  "name" : longest_substring,
  "min_price" : min(price),
  "max_price" : max(price)
}
print(group)
