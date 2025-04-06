import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.parametrize(
    'max_students,students_count,expected_status',
    [
        (20, 20, HTTP_200_OK),  # Успешный случай: ровно 20 студентов
        (20, 21, HTTP_400_BAD_REQUEST),  # Неудачный случай: 21 студент
        (10, 10, HTTP_200_OK),  # Успешный случай: ровно 10 студентов
        (10, 11, HTTP_400_BAD_REQUEST),  # Неудачный случай: 11 студентов
    ]
)
def test_max_students_limit(api_client, course_factory, student_factory, settings, max_students, students_count,
                            expected_status):
    """Тест ограничения количества студентов на курсе."""

    settings.MAX_STUDENTS_PER_COURSE = max_students

    course = course_factory()

    students = student_factory(_quantity=students_count)
    students_ids = [student.id for student in students]

    data = {
        'name': course.name,
        'students': students_ids
    }

    url = reverse('courses-detail', kwargs={'pk': course.id})
    response = api_client.put(url, data=data, format='json')

    # Проверяем результат
    assert response.status_code == expected_status
