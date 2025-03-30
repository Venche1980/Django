from django.urls import path
from .views import SensorListCreateView, SensorRetrieveUpdateView, MeasurementCreateView

urlpatterns = [
    # Получение списка всех датчиков и создание нового датчика
    path('sensors/', SensorListCreateView.as_view(), name='sensor-list'),

    # Получение подробной информации о конкретном датчике и ее обновление
    path('sensors/<int:pk>/', SensorRetrieveUpdateView.as_view(), name='sensor-detail'),

    # Добавление измерений
    path('measurements/', MeasurementCreateView.as_view(), name='measurement-create'),
]
