"""
เขียบนโปรแกรมแปลงตัวเลยเป็นตัวเลข roman

[Input]
number: list of numbers

[Output]
roman_text: roman number

[Example 1]
input = 101
output = CI

[Example 2]
input = -1
output = number can not less than 0
"""


class Solution:

    def number_to_roman(self, number: int) -> str:
        # 1. ดักจับค่าติดลบเหมือนเดิม
        if number < 0:
            return "number can not less than 0"
        if number == 0:
            return ""
        if number > 3999:
            return "According to the basic rules of the Roman numeral system, the maximum value does not exceed 3999."
            
        # 2. จับคู่ค่าตัวเลขกับสัญลักษณ์โรมัน (ใช้รูปแบบเหมือนเดิม)
        roman_mapping = [
            (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
            (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
            (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
        ]
        
        roman_text = [] # ใช้ List ในการเก็บตัวอักษรจะประหยัดเมมโมรี่กว่าการบวก String โดยตรง
        
        # 3. วนลูปคำนวณแบบข้ามขั้นตอน (ไม่ต้องใช้ while ซ้อนข้างในแล้ว)
        for value, symbol in roman_mapping:
            if number == 0:
                break # ถ้าค่าโดนหักจนเหลือ 0 แล้ว ให้หยุดทำงานทันทีเพื่อประหยัดรอบลูป
                
            if number >= value:
                count = number // value  # หาว่าต้องใส่ตัวอักษรนี้ทั้งหมดกี่ตัว (หารปัดเศษ)
                roman_text.append(symbol * count)  # ใช้ฟีเจอร์ Python คูณตัวอักษรเพิ่มตามจำนวนทีเดียว
                number %= value  # อัปเดตค่าตัวเลขที่เหลือโดยการหาเศษ
                
        return "".join(roman_text) # รวมตัวอักษรทั้งหมดใน List ออกมาเป็น String คำตอบ

# python 1_logic_test\4_number_to_roman\main.py
sol = Solution()

input = 101
result1 = sol.number_to_roman(input)
print(f"Input: {input} -> Output: {result1}")

input = -1
result2 = sol.number_to_roman(input)
print(f"Input: {input} -> Output: {result2}")

input = 1235
result2 = sol.number_to_roman(input)
print(f"Input: {input} -> Output: {result2}")