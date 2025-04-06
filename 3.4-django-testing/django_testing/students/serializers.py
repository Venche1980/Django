from rest_framework import serializers
from django.conf import settings

from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate_students(self, value):
        """Проверка, что количество студентов не превышает максимально допустимое."""
        if len(value) > settings.MAX_STUDENTS_PER_COURSE:
            raise serializers.ValidationError(
                f'Курс не может содержать более {settings.MAX_STUDENTS_PER_COURSE} студентов'
            )
        return value