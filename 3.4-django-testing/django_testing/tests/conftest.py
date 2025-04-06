import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student
from django.conf import settings


@pytest.fixture
def api_client():
    """Фикстура для API клиента."""
    return APIClient()


@pytest.fixture
def course_factory():
    """Фикстура для фабрики курсов."""
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    """Фикстура для фабрики студентов."""
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory