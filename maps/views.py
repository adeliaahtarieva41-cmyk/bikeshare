import json
from django.shortcuts import render
from django.conf import settings
from women.models import Bike


def map_view(request):
    # Координаты велосипедов (можно добавить в базу данных позже)
    bike_coords = {
        1: [55.795, 49.106],  # Городской - ул. Баумана
        2: [55.800, 49.120],  # Горный - ул. Кремлёвская
        3: [55.810, 49.150],  # Электро - пр. Победы
        4: [55.780, 49.080],  # Складной - ул. Профсоюзная
        5: [55.770, 49.100],  # Детский - ул. Ленина
        6: [55.788, 49.122],  # Тандем - парк Горького
        7: [55.820, 49.140],  # BMX - скейт-парк
    }

    bikes = Bike.objects.all()

    bikes_data = []
    for bike in bikes:
        coords = bike_coords.get(bike.id, [55.796127, 49.106405])  # центр Казани по умолчанию

        bikes_data.append({
            'id': bike.id,
            'name': bike.name,
            'address': bike.address,
            'price_per_hour': float(bike.price_per_hour),
            'url': bike.get_absolute_url(),
            'lat': coords[0],
            'lon': coords[1],
        })

    context = {
        'title': 'Велосипеды на карте',
        'bikes_json': json.dumps(bikes_data, ensure_ascii=False),
        'yandex_maps_api_key': settings.YANDEX_MAPS_API_KEY,
    }

    return render(request, 'maps/map.html', context)