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


iphone = "iPhone 14 Pro Max 128GB | Chính hãng VN/A"
iphone_list = [
    "iPhone 14 Pro Max 128gb",
    "điện thoại iPhone 14 Pro Max 128GB",
    "iPhone 14 Pro Max 128GB",
    "iPhone 14 Pro Max 128GB 123",
]

result = find_longest_common_subarray(iphone, iphone_list)
print("Mảng con giống nhau dài nhất:", result)
