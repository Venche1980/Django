import csv
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # Считываем данные из CSV-файла
    with open(settings.BUS_STATION_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        stations = list(reader)  # Преобразуем данные в список словарей

    # Пагинация
    paginator = Paginator(stations, 10)  # Показывать 10 остановок на странице
    page_number = request.GET.get('page', 1)  # Получаем номер страницы из параметров запроса
    page = paginator.get_page(page_number)

    # Формируем контекст
    context = {
        'bus_stations': [
            {
                'Name': station.get('Name', ''),
                'Street': station.get('Street', ''),
                'District': station.get('District', ''),
            }
            for station in page.object_list
        ],
        'page': page,  # Передаем объект пагинации
    }

    return render(request, 'stations/index.html', context)
