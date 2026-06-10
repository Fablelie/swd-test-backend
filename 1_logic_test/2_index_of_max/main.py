"""
เขียบนโปรแกรมหา index ของตัวเลขที่มีค่ามากที่สุดใน list

[Input]
numbers: list of numbers

[Output]
index: index of maximum number in list

[Example 1]
input = [1,2,1,3,5,6,4]
output = 5

[Example 2]
input = []
output = list can not blank
"""


class Solution:

    def find_max_index(self, numbers: list) -> int | str:
        if len(numbers) == 0:
            return "list can not blank"
        
        max_value = max(numbers)
        max_index = numbers.index(max_value)

        return max_index

    # ในกรณีที่อยากได้ index ของ max value ที่อยู่ใน list มากกว่า 1 ตัว
    def find_max_indexs(self, numbers: list) -> list | str:
        if len(numbers) == 0:
            return "list can not blank"
        
        max_value = max(numbers)
        result_indices = []

        for i in range(len(numbers)):
            if numbers[i] == max_value:
                result_indices.append(i)

        return result_indices
    
# python 1_logic_test\2_index_of_max\main.py
sol = Solution()

input = [1,2,1,3,5,6,4]
result1 = sol.find_max_index(input)
print(f"Input: {input} -> Output: {result1}")

input = [1,2,1,3,5,6,4,6]
result2 = sol.find_max_indexs(input)
print(f"Input: {input} -> Output: {result2}")