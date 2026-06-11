## 🚀 ขั้นตอนการติดตั้งและเปิดใช้งาน (Quick Start)

### 1. Virtual Environment
เปิด Terminal หรือ PowerShell มาที่ path `4_rest_api` จากนั้นพิมพ์คำสั่งสร้างและเปิดระบบ:
```bash
# สร้าง vn
py -3.10 -m venv .venv

# เปิดใช้งาน (สำหรับ Windows PowerShell)
.venv\Scripts\Activate.ps1

# เปิดใช้งาน (สำหรับ Mac / Linux Terminal)
source .venv/bin/activate

# ออกจาก .venv
deactivate
```

### 2. ติดตั้ง Library ทั้งหมดที่โปรเจกต์ต้องการ
เมื่อขึ้นสถานะ `(.venv)` ด้านหน้าบรรทัดแล้ว พิมพ์คำสั่งติดตั้งจากไฟล์ข้อกำหนด:
```bash
pip install -r requirements.txt
```

### 3. ประกอบร่างสร้างตารางฐานข้อมูล (Database Migration)
สั่งให้ Django สร้างตารางลงในไฟล์ SQLite:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. โหลดข้อมูลจำลองเริ่มต้น (Load Mock Data)
พิมพ์คำสั่งนี้เพื่อดึงข้อมูลโรงเรียน ห้องเรียน ครู และนักเรียนสำเร็จรูป เข้าสู่ฐานข้อมูลออฟไลน์ทันทีโดยไม่ต้องกดกรอกทีละช่อง:
```bash
python manage.py loaddata mock_data
```

**วิธีสร้างบัญชีแอดมินตัวแรกเพื่อล็อกอิน:**
```bash
python manage.py createsuperuser
```
**http://127.0.0.1:8000/admin**
ถ้าใช้ python version 3.14 จะเข้าใช้งานหน้า admin ไม่ได้

### 5. สั่งรันเซิร์ฟเวอร์ (Run Server)
```bash
python manage.py runserver
```
ระบบจะรันสำเร็จที่พิกัดลิงก์: **`http://127.0.0.1:8000/api/v1/`**

---

## 🌐 รายชื่อเส้นทาง API (Endpoints) และวิธีการเรียกใช้งาน

เข้าใช้งานผ่านเว็บเบราว์เซอร์:

### 🏛️ 1. School API
*   **ดูรายชื่อทั้งหมด / สร้าง (List/Create):** `GET` / `POST` ➡️ `http://127.0.0.1:8000/api/v1/schools/`
*   **Filter:** ค้นหาด้วยชื่อโรงเรียน ➡️ `?name=ชื่อโรงเรียน`
*   **Detail:** `GET` ➡️ `http://127.0.0.1:8000/api/v1/schools/<id>/`
    *   *ข้อมูลจะแสดง:* `count_of_classroom`, `count_of_teacher`, และ `count_of_student` ให้โดยอัตโนมัติ

### 🏫 2. Classroom API
*   **ดูรายชื่อทั้งหมด / สร้าง (List/Create):** `GET` / `POST` ➡️ `http://127.0.0.1:8000/api/v1/classrooms/`
*   **Filter:** ค้นหาตามไอดีโรงเรียนสังกัด ➡️ `?school=<id_school>`
*   **Detail:** `GET` ➡️ `http://127.0.0.1:8000/api/v1/classrooms/<id>/`
    *   *ข้อมูลจะแสดง:* `teachers` (ลิสต์รายชื่อครูในห้อง) และ `students` (ลิสต์รายชื่อนักเรียนในห้อง)

### 👨‍🏫 3. Teacher API
*   **ดูรายชื่อทั้งหมด / สร้าง (List/Create):** `GET` / `POST` ➡️ `http://127.0.0.1:8000/api/v1/teachers/`
*   **Filters:** สามารถผสมตัวแปรค้นหาได้ ➡️ `?school=1&classrooms=1&firstname=สมชาย&lastname=สายสอน&gender=M`
*   **Detail:** `GET` ➡️ `http://127.0.0.1:8000/api/v1/teachers/<id>/`
    *   *ข้อมูลจะออกมาเป็น:* `classrooms_detail` (ลิสต์รายละเอียดห้องเรียนทั้งหมดที่คุณครูคนนี้รับผิดชอบ)

### 🧑‍🎓 4. Student API
*   **ดูรายชื่อทั้งหมด / สร้าง (List/Create):** `GET` / `POST` ➡️ `http://127.0.0.1:8000/api/v1/students/`
*   **Filters:** สามารถผสมตัวแปรค้นหาได้ ➡️ `?school=1&classroom=1&firstname=กิตติ&lastname=เรียนดี&gender=M`
*   **Detail:** `GET` ➡️ `http://127.0.0.1:8000/api/v1/students/<id>/`
    *   *ข้อมูลจะออกมาเป็น:* `classroom_detail` (รายงานบอกชั้นปีและห้องที่นักเรียนคนนี้อยู่)

---

## 🧪 Automated Tests

ทดสอบ CRUD และ Filter ว่าทำงานได้ถูกต้อง:
```bash
python manage.py test
```
