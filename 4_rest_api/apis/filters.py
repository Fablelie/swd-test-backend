from django_filters import FilterSet, filters
from .models import School, Classroom, Teacher, Student

# code here
class SchoolFilter(FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = School
        fields = ['name']

class ClassroomFilter(FilterSet):
    class Meta:
        model = Classroom
        fields = ['school']

class TeacherFilter(FilterSet):
    # เชื่อมหาไอดีโรงเรียนผ่าน classrooms
    school = filters.NumberFilter(field_name='classrooms__school', lookup_expr='exact')
    classrooms = filters.NumberFilter(field_name='classrooms__id', lookup_expr='exact')
    firstname = filters.CharFilter(lookup_expr='icontains')
    lastname = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Teacher
        fields = ['school', 'classrooms', 'firstname', 'lastname', 'gender']

class StudentFilter(FilterSet):
    # เชื่อมหาไอดีโรงเรียนผ่าน classroom
    school = filters.NumberFilter(field_name='classroom__school', lookup_expr='exact')
    firstname = filters.CharFilter(lookup_expr='icontains')
    lastname = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Student
        fields = ['school', 'classroom', 'firstname', 'lastname', 'gender']
