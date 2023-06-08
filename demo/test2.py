def find_longest_common_substring(string, array):
    m = len(string)
    max_length = 0
    end_index = 0

    for i in range(m):
        for sub_array in array:
            n = len(sub_array)
            lengths = [[0] * (n + 1) for _ in range(m + 1)]

            for j in range(1, m + 1):
                for k in range(1, n + 1):
                    if string[j - 1] == sub_array[k - 1]:
                        lengths[j][k] = lengths[j - 1][k - 1] + 1
                        if lengths[j][k] > max_length:
                            max_length = lengths[j][k]
                            end_index = j

    start_index = end_index - max_length

    return string[start_index:end_index]
import pymongo
import re
client = pymongo.MongoClient('mongodb+srv://user:123456Aa@cluster0.t3aqomt.mongodb.net')
db = client['shops']
category = db.categories.find_one({"name": 'iphone'})

iphone = "iphone 14 128gb".replace("(", "").replace(")", "")
store_id = "4883128f5159462fa63340991805885b"
print(iphone)
datas = list(db.products.find({"category_id": category["_id"],"store_id": {"$nin": [store_id]} }).distinct("name"))
longest_substring = find_longest_common_substring(iphone, datas)
print("Longest common substring:", longest_substring)
datas = list(db.products.find({"category_id": category["_id"],"store_id": {"$nin": [store_id]}},{"name":1,"price":1,"store_id":1}))
price = []
list_data = []
for item in datas:
  name = item["name"].replace("(", "").replace(")","")
  if longest_substring in name:
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
