from typing import Optional

import requests
from django.conf import settings


def get_city_coordinates(city_name: str) -> Optional[tuple]:
    """Получение координат по названию города"""
    geocoder_url = "https://geocode-maps.yandex.ru/1.x/"
    params = {
        "geocode": city_name,
        "apikey": settings.YANDEX_GEOCODER_API_KEY,
        "kind": "locality",
        "lang": "ru_RU",
        "format": "json",
    }
    response = requests.get(geocoder_url, params=params)
    if response.status_code == 200:
        response_data = response.json()
        feature_member = response_data["response"]["GeoObjectCollection"][
            "featureMember"
        ]
        if feature_member:
            coordinates_str = feature_member[0]["GeoObject"]["Point"]["pos"]
            longitude, latitude = map(float, coordinates_str.split())
            return longitude, latitude
    return None


def get_weather_data(location: tuple) -> Optional[dict]:
    """Получение текущей погоды по координатам"""
    weather_url = "https://api.weather.yandex.ru/v2/forecast"
    headers = {
        "X-Yandex-API-Key": settings.YANDEX_WEATHER_API_KEY,
    }
    params = {
        "lat": location[1],
        "lon": location[0],
        "lang": "ru_RU",
    }
    response = requests.get(weather_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    return None


def get_weather_data_by_city_name(city: str) -> Optional[dict]:
    """Получение текущей погоды по названию города/посёлка"""
    location = get_city_coordinates(city)
    if not location:
        return None

    weather_api_data = get_weather_data(location)
    if not weather_api_data:
        return None

    return weather_api_data
