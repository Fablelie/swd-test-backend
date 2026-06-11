from django.db import models

# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=255, unique=True) # ห้ามชื่อซ้ำ
    abbreviation = models.CharField(max_length=10, unique=True) # ตัวย่อห้ามซ้ำ
    address = models.TextField()

    def __str__(self):
        return self.name

class Classroom(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classrooms')
    grade = models.IntegerField()
    section = models.IntegerField()

    def __str__(self):
        return f"{self.school.abbreviation} - {self.grade}/{self.section}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['school', 'grade', 'section'],
                name='unique_classroom_in_school'
            ) # โรงเรียนเดี่ยวกันห้ามมีช
        ]

class Teacher(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    classrooms = models.ManyToManyField(Classroom, related_name='teachers')

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['firstname', 'lastname'],
                name='unique_teacher_name'
            ) # ชื่อซ้ำได้ นามสกุลซ้ำได้ แต่ห้ามซ้ำพร้อมกันทั้งสองอย่าง
        ]

class Student(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['firstname', 'lastname'],
                name='unique_student_name'
            ) # ชื่อซ้ำได้ นามสกุลซ้ำได้ แต่ห้ามซ้ำพร้อมกันทั้งสองอย่าง
        ]