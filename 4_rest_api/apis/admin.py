from django.contrib import admin
from .models import School, Classroom, Teacher, Student

# Register your models here.
@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'abbreviation')
    search_fields = ('name', 'abbreviation')

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('id', 'school', 'grade', 'section')
    list_filter = ('school', 'grade')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname', 'gender')
    search_fields = ('firstname', 'lastname')
    list_filter = ('gender',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname', 'gender', 'classroom')
    search_fields = ('firstname', 'lastname')
    list_filter = ('gender', 'classroom__school')