from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from apis.models import Student
from apis.serializers import StudentSerializer
from apis.filters import StudentFilter

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentFilter
