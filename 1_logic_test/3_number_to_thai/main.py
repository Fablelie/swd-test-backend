"""
เขียบนโปรแกรมแปลงตัวเลยเป็นคำอ่านภาษาไทย

[Input]
number: positive number rang from 0 to 10_000_000

[Output]
num_text: string of thai number call

[Example 1]
input = 101
output = หนึ่งร้อยเอ็ด

[Example 2]
input = -1
output = number can not less than 0
"""


class Solution:

    def number_to_thai(self, number: int) -> str:
        if number < 0:
            return "number can not less than 0"
        if number == 0:
            return "ศูนย์"

        # ฟังก์ชันย่อยสำหรับแปลงเลขกลุ่มย่อย (0-999,999) ให้เป็นคำอ่านภาษาไทย
        def _convert_under_million(n):
            if n == 0:
                return ""
            
            # ลิสต์คำอ่านแบบถูกต้องตามตำแหน่งหลัก
            th_digits = ["", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
            th_positions = ["", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน"]
            
            text = ""
            num_str = str(n)
            length = len(num_str)
            
            for i in range(length):
                digit = int(num_str[i])
                pos = length - 1 - i
                
                if digit == 0:
                    continue
                
                # กฎพิเศษภาษาไทย
                if pos == 0 and digit == 1 and length > 1:
                    text += "เอ็ด"
                elif pos == 1 and digit == 2:
                    text += "ยี่สิบ"
                elif pos == 1 and digit == 1:
                    text += "สิบ"
                else:
                    text += th_digits[digit] + th_positions[pos]
            return text

        # --- ส่วนหลักการคำนวณแยกสเกลล้าน ---
        result = ""
        
        # 1. จัดการกลุ่มที่เกินล้าน (ล้าน, สิบล้าน)
        if number >= 1000000:
            million_part = number // 1000000
            result += _convert_under_million(million_part) + "ล้าน"
            number %= 1000000  # เก็บเศษที่เหลือต่ำกว่าล้านไว้ทำต่อ
            
        # 2. จัดการกลุ่มที่เหลือต่ำกว่าล้าน (แสน, หมื่น, พัน, ร้อย, สิบ, หน่วย)
        if number > 0:
            # ตรวจสอบกฎพิเศษ: ถ้ามีหลักล้านอยู่ข้างหน้า และเหลือเลข 1 ในหลักหน่วยตัวสุดท้าย
            if result != "" and number == 1:
                result += "เอ็ด"
            else:
                result += _convert_under_million(number)
                
        return result

# python 1_logic_test\3_number_to_thai\main.py
sol = Solution()

input = 101
result1 = sol.number_to_thai(input)
print(f"Input: {input} -> Output: {result1}")

input = -1
result2 = sol.number_to_thai(input)
print(f"Input: {input} -> Output: {result2}")

input = 1112121
result2 = sol.number_to_thai(input)
print(f"Input: {input} -> Output: {result2}")