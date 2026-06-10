"""
เขียบนโปรแกรมหาจำนวนเลข 0 ที่ออยู่ติดกันหลังสุดของค่า factorial โดยห้ามใช้ function from math

[Input]
number: as an integer

[Output]
count: count of tailing zero as an integer

[Example 1]
input = 7
output = 1

[Example 2]
input = -10
output = number can not be negative
"""


class Solution:

    def find_tailing_zeroes(self, number: int) -> int | str:
        if number < 0:
            return "number can not be negative"
        
        target_digit = 0
        count = 0
        
        # แบบเข้าใจยาก
        # Legendre's Formula ไม่รองรับถ้าโจยท์เปลี่ยนเป็นหาเลขอื่น
        i = 5
        # loop ไปเรื่อยๆเพื่อหาว่า number หารด้วย i แล้วยังมากกว่า 1 อยู่ไหม
        while number // i >= 1:
        #   เอาผลหารปัดเศษแต่ละรอบมาเพิ่มจำนวนนับ (เพื่อหาว่ามีเลข 5 ซ่อนอยู่กี่ตัว)
            count += number // i
        #   เพิ่มตัวหารอีก 5 เท่าเพื่อเก็บเลข 5 ในชั่นที่ลึกขึ้นเช่น
        #   25! ถ้า 5, 10, 15, 20, 25 เราจะได้เลข 5 มา 5 ตัวแต่ใน 25 มี 2 ตัวเราเลยต้องเพิ่มตัวหารอีก 5 เท่าเพื่อเก็บเลข 5 ตัวที่ 2 จาก 25
        #   5, 25, 125, ... ไปเรื่อยๆ จนกว่า number // i < 1
            i *= 5

        ##################################################################
        # แบบอ่านง่ายเข้าใจง่าย
        # หาค่า Factorial
        # factorial_result = 1
        # for i in range(1, number + 1):
        #     factorial_result *= i

        # # แปลง factorial_result เป็น string
        # factorial_str = str(factorial_result)
        # # แปลง target_digit เป็น string
        # target_str = str(target_digit)

        # # revert loop ทีละ character เพื่อหาเลขที่เราต้องการว่าติดกันกี่ตัว
        # for char in reversed(factorial_str):
        #     if char == target_str:
        #         count += 1
        #     else:
        #         break

        return count

sol = Solution()

input = 7
result1 = sol.find_tailing_zeroes(input)
print(f"Input: {input} -> Output: {result1}")

input = -10
result2 = sol.find_tailing_zeroes(input)
print(f"Input: {input} -> Output: {result2}")
