import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory):
    """Тест на получение одного курса """

    course = course_factory()

    url = reverse('courses-detail', kwargs={'pk': course.id})
    response = api_client.get(url)

    assert response.status_code == HTTP_200_OK
    assert response.data['id'] == course.id
    assert response.data['name'] == course.name


@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    """Тест на получение списка курсов """

    courses = course_factory(_quantity=10)

    url = reverse('courses-list')
    response = api_client.get(url)

    assert response.status_code == HTTP_200_OK
    assert len(response.data) == len(courses)


@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    """Тест на фильтрацию списка курсов по id."""

    courses = course_factory(_quantity=10)
    course_id = courses[0].id

    url = reverse('courses-list')
    response = api_client.get(url, data={'id': course_id})

    assert response.status_code == HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['id'] == course_id


@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    """Тест на фильтрацию списка курсов по name."""

    course_factory(_quantity=9)
    course = course_factory(name='Специальный курс')

    url = reverse('courses-list')
    response = api_client.get(url, data={'name': 'Специальный курс'})

    assert response.status_code == HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Специальный курс'


@pytest.mark.django_db
def test_create_course(api_client):
    """Тест на успешное создание курса."""

    data = {
        'name': 'Новый курс'
    }

    url = reverse('courses-list')
    response = api_client.post(url, data=data, format='json')

    assert response.status_code == HTTP_201_CREATED
    assert response.data['name'] == 'Новый курс'


@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    """Тест на успешное обновление курса."""
    course = course_factory()

    data = {
        'name': 'Обновленный курс'
    }

    url = reverse('courses-detail', kwargs={'pk': course.id})
    response = api_client.put(url, data=data, format='json')

    assert response.status_code == HTTP_200_OK
    assert response.data['name'] == 'Обновленный курс'


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    """Тест на успешное удаление курса."""
    course = course_factory()

    url = reverse('courses-detail', kwargs={'pk': course.id})
    response = api_client.delete(url)

    assert response.status_code == HTTP_204_NO_CONTENT
