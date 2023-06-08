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

# Test
string = "abcdef"
array = ["xyabc", "abcmno", "pqrabcde"]
longest_substring = find_longest_common_substring(string, array)
print("Longest common substring:", longest_substring)
