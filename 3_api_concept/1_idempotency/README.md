## Question
![](/assets/q_idempotency.png)
## Response Section

ความหายของ Idemptency ใน RESTful API
    คุณสมบัติของ API ที่ไม่ว่าจะถูกเรียกใช้งานซ้ำกี่ครั้งด้วยข้อมูลเดิม ผลลัพธ์บนระบบและสถานะของเซิร์ฟเวอร์จะต้องยังคงเท่าเดิม เหมือนกับการเรียกใช้งานสำเร็จในครั้งแรก หลักๆเลยก็หากมี Post ส่งมาหลายๆครั้งด้วยจุดประสงค์เดี่ยวกันระบบจะต้องให้ทำแค่ครั้งแรกเท่านั้น

#######################################################################################
ตัวอย่าง code

import uuid
from fastapi import FastAPI, Header, HTTPException
import redis

app = FastAPI()

# เชื่อมต่อกับ Redis (สมมุติว่ารันในเพอร์ต 6379)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

@app.post("/api/v1/payments")
def create_payment(
    amount: int, 
    idempotency_key: str = Header(None) # รับคีย์จาก Header ของผู้ใช้
):
    # บังคับว่าต้องส่ง Idempotency-Key มาใน Header ทุกครั้ง
    if not idempotency_key:
        raise HTTPException(status_code=400, detail="Missing Idempotency-Key header")

    # ตรวจสอบใน Redis ว่าคีย์นี้เคยถูกส่งมาทำงานหรือยัง
    existing_response = r.get(idempotency_key)
    
    if existing_response:
        # ถ้าเจอคีย์เดิม แปลว่าเป็นการส่งซ้ำ! 
        # ส่งผลลัพธ์เก่ากลับไปทันทีโดยไม่ต้องไปหักเงินซ้ำในระบบ
        return {
            "status": "success",
            "message": f"Retrieved from cache (Duplicate Request)",
            "transaction_id": existing_response
        }

    # ถ้านี่คือคีย์ใหม่ (การทำงานครั้งแรก) -> run business logic
    # จำลองการสร้าง Transaction ID ของการหักเงิน
    new_transaction_id = str(uuid.uuid4())
    
    # ... business logic here!! ...

    # บันทึกผลลัพธ์นี้ลง Redis ผูกกับคีย์ไว้ 
    # และตั้งเวลาหมดอายุ (เช่น อยู่ได้ 1 วัน หรือ 86400 วินาที) เพื่อไม่ให้ขยะเต็มระบบ
    r.setex(idempotency_key, 86400, new_transaction_id)

    # ส่งคำตอบกลับไปให้ผู้ใช้งานในครั้งแรก
    return {
        "status": "success",
        "message": "Payment processed successfully",
        "transaction_id": new_transaction_id
    }