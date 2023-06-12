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

def is_subarray_in_string(subarray, string):
    subarray_set = set(subarray)
    string_set = set(string.split())
    return subarray_set.issubset(string_set)

iphone_list = [
    {"id": 1, "name":"iPhone 14 128gb"},
    {"id": 1, "name":"iPhone 13 64gb"},
    {"id": 1, "name":"iPhone 12 64gb"},
    {"id": 1, "name":"iPhone 11 64gb"},
]

iphone_list1 = [
    {"id": 2, "name":"iPhone 14 128gb | Chính hãng VN/A"},
    {"id": 2, "name":"iPhone 13 64gb | Chính hãng VN/A"},
    {"id": 2, "name":"iPhone 12 64gb | Chính hãng VN/A"},
    {"id": 2, "name":"iPhone 11 64gb | Chính hãng VN/A"},
]

iphone_list2 = [
    {"id": 3, "name":"iPhone 14 128gb"},
    {"id": 3, "name":"iPhone 13 64gb"},
    {"id": 3, "name":"iPhone 12 64gb"},
    {"id": 3, "name":"iPhone 11 128gb"},
]

listip = iphone_list1 + iphone_list2 + iphone_list
datas = []
ids = [1,2,3]
tmp = []
for i in ids:
    list3 = []
    list1 = [obj for obj in listip if obj["id"] == i]
    if tmp:
        list3 = [a for a in list3 if a in tmp]
    else:
        list3 = list1
    for item in list3:
        data = []
        list2 = [obj["name"] for obj in listip if obj["id"] != i]
        result = find_longest_common_subarray(item["name"], list2)
        if result:
            for ilist in listip:
                name = is_subarray_in_string(result,ilist["name"])
                if name:
                    data.append(ilist["name"])
                    tmp.append(ilist["name"])
        datas.append(data)
for item in listip:
    if not item["name"] in tmp:
        datas.append([item["name"]])
print(datas)