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
        substring = longest_common_substring(string, s)
        if len(substring) > max_length:
            max_length = len(substring)
            longest_substring = substring

    return longest_substring


iphone_list = [
    "iPhone 14 Pro Max 128gb",
    "điện thoại iPhone 14 Pro Max 128GB",
    "iPhone 14 Pro Max 128GB",
    "iPhone 14 Pro Max 128GB 123",
]
longest_substring = find_longest_substring("iPhone 14 Pro Max 128GB | Chính hãng VN/A", iphone_list)

print("Chuỗi con lớn nhất:", longest_substring)

