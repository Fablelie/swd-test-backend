from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import School, Classroom, Teacher, Student

class SchoolSystemComprehensiveTests(APITestCase):
    
    def setUp(self):
        """1. เตรียมข้อมูลพื้นฐานจำลองสำหรับการทดสอบ"""
        # สร้างโรงเรียน 2 แห่ง (แห่งที่ 2 เอาไว้ใช้เทสระบบ Filter ค้นหาตัวกรอง)
        self.school_a = School.objects.create(name="โรงเรียนสุขใจ", abbreviation="สจ.", address="กรุงเทพฯ")
        self.school_b = School.objects.create(name="โรงเรียนเรียนดี", abbreviation="รด.", address="นนทบุรี")

        # สร้างห้องเรียน
        self.classroom_a1 = Classroom.objects.create(school=self.school_a, grade=1, section=1)
        self.classroom_a2 = Classroom.objects.create(school=self.school_a, grade=1, section=2)
        self.classroom_b1 = Classroom.objects.create(school=self.school_b, grade=2, section=1)

        # สร้างคุณครู
        self.teacher_m = Teacher.objects.create(firstname="สมชาย", lastname="สายสอน", gender="M")
        self.teacher_f = Teacher.objects.create(firstname="สมศรี", lastname="ดีเด่น", gender="F")
        # ครูสมชายสอนห้อง a1 และ a2 / ครูสมศรีสอนห้อง b1
        self.teacher_m.classrooms.add(self.classroom_a1, self.classroom_a2)
        self.teacher_f.classrooms.add(self.classroom_b1)

        # สร้างนักเรียน
        self.student_m = Student.objects.create(firstname="เด็กชายกิตติ", lastname="เรียนดี", gender="M", classroom=self.classroom_a1)
        self.student_f = Student.objects.create(firstname="เด็กหญิงนภา", lastname="ใจใส", gender="F", classroom=self.classroom_a1)

        # ลงทะเบียนคีย์ลัดเส้นทาง URL หลักของแต่ละ API (ดึงจาก Namespace 'v1')
        self.school_urls = {'list': reverse('v1:school-list'), 'detail': lambda pk: reverse('v1:school-detail', kwargs={'pk': pk})}
        self.classroom_urls = {'list': reverse('v1:classroom-list'), 'detail': lambda pk: reverse('v1:classroom-detail', kwargs={'pk': pk})}
        self.teacher_urls = {'list': reverse('v1:teacher-list'), 'detail': lambda pk: reverse('v1:teacher-detail', kwargs={'pk': pk})}
        self.student_urls = {'list': reverse('v1:student-list'), 'detail': lambda pk: reverse('v1:student-detail', kwargs={'pk': pk})}

        test_user = User.objects.create_user(username='tester', password='password123')
        self.client.force_authenticate(user=test_user)

    # ==========================================
    # 1. SCHOOL API TESTS
    # ==========================================
    def test_school_crud(self):
        """ทดสอบ Create, Update, Delete ของ School"""
        # Test Create (POST)
        data = {"name": "โรงเรียนวิทยาศาสตร์", "abbreviation": "วท.", "address": "ปทุมธานี"}
        response = self.client.post(self.school_urls['list'], data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Test Update (PUT)
        detail_url = self.school_urls['detail'](self.school_a.id) # โรงเรียนสุขใจ
        update_data = {"name": "โรงเรียนสุขใจวิทยา", "abbreviation": "สจว.", "address": "กรุงเทพฯ"}
        response = self.client.put(detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(School.objects.get(id=self.school_a.id).name, "โรงเรียนสุขใจวิทยา")

        # Test Delete (DELETE)
        response = self.client.delete(detail_url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT])
        self.assertEqual(School.objects.filter(id=self.school_a.id).count(), 0)

    def test_school_list_and_filter(self):
        """ทดสอบดูรายการโรงเรียนทั้งหมด และการกรองด้วยชื่อ"""
        # Test Filter by name
        # ค้นหาคำว่า 'สุขใจ' (ควรเจอโรงเรียนเดียว)
        response = self.client.get(self.school_urls['list'], {'name': 'สุขใจ'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['abbreviation'], 'สจ.')

    def test_school_detail_counts(self):
        """ทดสอบข้อมูลเจาะลึกโรงเรียน ต้องมีเลขนับจำนวนนับ ห้อง/ครู/นักเรียน ที่ถูกต้อง"""
        # Test Get count of classroom, teacher, student
        response = self.client.get(self.school_urls['detail'](self.school_a.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count_of_classroom'], 2) # มีห้อง a1, a2
        self.assertEqual(response.data['count_of_teacher'], 1)   # มีครูสมชาย 1 คน
        self.assertEqual(response.data['count_of_student'], 2)   # มีนักเรียน 2 คน

    # ==========================================
    # 2. CLASSROOM API TESTS
    # ==========================================
    def test_classroom_crud(self):
        """[Classroom] ทดสอบระบบปฏิบัติการพื้นฐาน (Create -> Update -> Delete)"""
        # Classroom Create
        create_data = {"school": self.school_a.id, "grade": 3, "section": 5}
        response = self.client.post(self.classroom_urls['list'], create_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_room_id = response.data['id']

        # Classroom Update
        update_url = self.classroom_urls['detail'](new_room_id)
        update_data = {"school": self.school_a.id, "grade": 3, "section": 9}
        response = self.client.put(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Classroom Delete
        response = self.client.delete(update_url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT])

    def test_classroom_detail_lists(self):
        """[Classroom Detail] แยกทดสอบโครงสร้างภายในของข้อมูลเจาะลึก ว่ามีลิสต์ครูและนักเรียนไหม"""
        # Classroom Get detail
        response = self.client.get(self.classroom_urls['detail'](self.classroom_a1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('teachers' in response.data)
        self.assertTrue('students' in response.data)

    def test_classroom_filter_by_school(self):
        """ทดสอบการกรองห้องเรียนด้วยไอดีโรงเรียน"""
        # get Classroom filter by school
        # กรองเอาเฉพาะห้องเรียนของโรงเรียนบี (ควรเจอ 1 ห้อง)
        response = self.client.get(self.classroom_urls['list'], {'school': self.school_b.id}, format='json') # filter จากโรงเรียนเรียนดี
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['grade'], 2)

    # ==========================================
    # 3. TEACHER API TESTS
    # ==========================================
    def test_teacher_crud(self):
        """[Teacher] ทดสอบระบบปฏิบัติการตามตรรกะ (สร้างครูวิชา -> อัปเดตผูกห้องเพิ่ม -> ลบทิ้ง)"""
        # Teacher Create (เพิ่มครูวิชาแบบผูก 1 ห้อง)
        create_data = {"firstname": "วิชา", "lastname": "ความรู้ดี", "gender": "M", "classrooms": [self.classroom_a1.id]}
        response = self.client.post(self.teacher_urls['list'], create_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        teacher_id = response.data['id']

        # Teacher Update (อัปเดตผูกห้องเพิ่มเป็น 3 ห้อง)
        detail_url = self.teacher_urls['detail'](teacher_id)
        update_data = {"firstname": "วิชา", "lastname": "ความรู้ดี", "gender": "M", "classrooms": [self.classroom_a1.id, self.classroom_a2.id, self.classroom_b1.id]}
        response = self.client.put(detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Teacher Delete
        response = self.client.delete(detail_url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT])

    def test_teacher_detail_classroom_list(self):
        """[Teacher Detail] แยกทดสอบหน้าข้อมูลลึก ว่าแยกรายละเอียดห้องเรียนออกมาครบถ้วนไหม"""
        # Teacher get list of classroom
        teacher = self.teacher_f
        teacher.classrooms.add(self.classroom_a1, self.classroom_a2)

        response = self.client.get(self.teacher_urls['detail'](teacher.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['classrooms_detail']), 3) # classroom a1, a2, b1(ใน setup)

    def test_teacher_filters(self):
        """[Teacher Filter] แยกทดสอบตัวกรองค้นหาประวัติครู (school, classroom, firstname, lastname, gender)"""
        # สร้างครูจำลองสำหรับการทดสอบระบบ Filter ย่อย
        teacher_test = Teacher.objects.create(firstname="สมจิต", lastname="ใจมั่น", gender="M")
        teacher_test.classrooms.add(self.classroom_a1)

        filter_params = {
            'school': self.school_a.id,
            'classrooms': self.classroom_a1.id,
            'firstname': 'สมจิต',
            'lastname': 'ใจมั่น',
            'gender': 'M'
        }

        # เทสกรองด้วย filter_params
        response = self.client.get(self.teacher_urls['list'], filter_params, format='json')
        self.assertEqual(len(response.data), 1)

        # เทสกรองด้วยโรงเรียน (School ID)
        response = self.client.get(self.teacher_urls['list'], {'school': self.school_a.id}, format='json')
        self.assertEqual(len(response.data), 2) # สมจิต, สมชาย

        # เทสกรองด้วยห้องเรียน (Classroom ID)
        response = self.client.get(self.teacher_urls['list'], {'classrooms': self.classroom_a1.id}, format='json')
        self.assertEqual(len(response.data), 2) # สมจิต, สมชาย

        # เทสกรองด้วยชื่อคำบางส่วน (Firstname)
        response = self.client.get(self.teacher_urls['list'], {'firstname': 'จิต'}, format='json')
        self.assertEqual(response.data[0]['firstname'], 'สมจิต')

        # เทสกรองด้วยนามสกุลคำบางส่วน (Lastname)
        response = self.client.get(self.teacher_urls['list'], {'lastname': 'มั่น'}, format='json')
        self.assertEqual(response.data[0]['lastname'], 'ใจมั่น')

        # เทสกรองด้วยเพศ (Gender)
        response = self.client.get(self.teacher_urls['list'], {'gender': 'M'}, format='json')
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['firstname'], 'สมชาย')
        self.assertEqual(response.data[1]['firstname'], 'สมจิต')

    # ==========================================
    # 4. STUDENT API TESTS
    # ==========================================
    def test_student_crud(self):
        """[Student] ทดสอบระบบปฏิบัติการพื้นฐาน (Create -> Update -> Delete)"""
        # Create
        create_data = {"firstname": "มานะ", "lastname": "พากเพียร", "gender": "M", "classroom": self.classroom_a1.id}
        response = self.client.post(self.student_urls['list'], create_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        student_id = response.data['id']

        # Update
        detail_url = self.student_urls['detail'](student_id)
        update_data = {"firstname": "มานะ", "lastname": "พากเพียร", "gender": "M", "classroom": self.classroom_a2.id}
        response = self.client.put(detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Delete
        response = self.client.delete(detail_url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT])

    def test_student_detail_classroom_info(self):
        """[Student Detail] แยกทดสอบว่าในหน้าข้อมูลลึก มีหัวข้อรายงานห้องเรียนสังกัดอยู่ถูกต้องไหม"""
        student = Student.objects.create(firstname="ปิติ", lastname="ใจดี", gender="M", classroom=self.classroom_a1)
        response = self.client.get(self.student_urls['detail'](student.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('classroom_detail' in response.data)
        self.assertEqual(response.data['classroom_detail']['grade'], 1)

    def test_student_filters(self):
        """[Student Filter] แยกทดสอบระบบตัวกรองค้นหาประวัตินักเรียน (school, classroom, firstname, lastname, gender)"""
        # สร้างนักเรียนจำลองสำหรับการทดสอบระบบ Filter
        Student.objects.create(firstname="เด็กหญิงชูใจ", lastname="เลิศล้ำ", gender="F", classroom=self.classroom_a1)

        filter_params = {
            'school': self.school_a.id,
            'classrooms': self.classroom_a1.id,
            'gender': 'M'
        }

        # เทสกรองด้วย filter_params
        response = self.client.get(self.student_urls['list'], filter_params, format='json')
        self.assertEqual(len(response.data), 1) # กิตติ

        # เทสกรองด้วยโรงเรียน (School ID)
        response = self.client.get(self.student_urls['list'], {'school': self.school_a.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3) # กิตติ, นภา, ชูใจ

        # เทสกรองด้วยห้องเรียน (Classroom ID)
        response = self.client.get(self.student_urls['list'], {'classroom': self.classroom_a1.id}, format='json')
        self.assertEqual(len(response.data), 3) # กิตติ, นภา, ชูใจ

        response = self.client.get(self.student_urls['list'], {'classroom': self.classroom_a2.id}, format='json')
        self.assertEqual(len(response.data), 0) # ห้องว่างเรียนกับใคร

        # เทสกรองด้วยชื่อคำบางส่วน (Firstname)
        response = self.client.get(self.student_urls['list'], {'firstname': 'ชูใจ'}, format='json')
        self.assertEqual(response.data[0]['firstname'], 'เด็กหญิงชูใจ')

        # เทสกรองด้วยนามสกุลคำบางส่วน (Lastname)
        response = self.client.get(self.student_urls['list'], {'lastname': 'ล้ำ'}, format='json')
        self.assertEqual(response.data[0]['lastname'], 'เลิศล้ำ')

        # เทสกรองด้วยเพศ (Gender)
        response = self.client.get(self.student_urls['list'], {'gender': 'F'})
        self.assertEqual(len(response.data), 2) # นภา, ชูใจ

# print response debug
# print("\n=== OPEN READING RESPONSE.DATA ===")
# import json
# print(json.dumps(response.data, indent=4, ensure_ascii=False))
# print("======================================\n")