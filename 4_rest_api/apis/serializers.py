from rest_framework import serializers


# code here
from .models import School, Classroom, Teacher, Student

# --- เซอเรียลไลเซอร์ย่อย (Read Only) สำหรับซ้อนในหน้าข้อมูลละเอียด ---
class SimpleClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'grade', 'section']

class SimpleTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'firstname', 'lastname', 'gender']

class SimpleStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'firstname', 'lastname', 'gender']

# --- เซอเรียลไลเซอร์หลักใช้งานบน API ---
class SchoolSerializer(serializers.ModelSerializer):
    count_of_classroom = serializers.SerializerMethodField()
    count_of_teacher = serializers.SerializerMethodField()
    count_of_student = serializers.SerializerMethodField()

    class Meta:
        model = School
        fields = ['id', 'name', 'abbreviation', 'address', 'count_of_classroom', 'count_of_teacher', 'count_of_student']

    def get_count_of_classroom(self, obj):
        return obj.classrooms.count()

    def get_count_of_teacher(self, obj):
        return Teacher.objects.filter(classrooms__school=obj).distinct().count()

    def get_count_of_student(self, obj):
        return Student.objects.filter(classroom__school=obj).count()


class ClassroomSerializer(serializers.ModelSerializer):
    # ดึงรายชื่อครูและนักเรียนแสดงอัตโนมัติเมื่อดูรายละเอียด (Detail)
    teachers = SimpleTeacherSerializer(many=True, read_only=True)
    students = SimpleStudentSerializer(many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = ['id', 'school', 'grade', 'section', 'teachers', 'students']


class TeacherSerializer(serializers.ModelSerializer):
    classrooms_detail = SimpleClassroomSerializer(source='classrooms', many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = ['id', 'firstname', 'lastname', 'gender', 'classrooms', 'classrooms_detail']
        extra_kwargs = {'classrooms': {'write_only': True}} # ตอนส่ง POST/PUT รับอาเรย์ไอดีห้องเรียนกลมๆ เข้ามา


class StudentSerializer(serializers.ModelSerializer):
    classroom_detail = SimpleClassroomSerializer(source='classroom', read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'firstname', 'lastname', 'gender', 'classroom', 'classroom_detail']
        extra_kwargs = {'classroom': {'write_only': True}} # รับไอดีห้องเรียนหลัก
