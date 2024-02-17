from typing import Optional

from .api_services import get_weather_data_by_city_name
from .models import WeatherData


def get_or_create_weather_data(city: str) -> Optional[WeatherData]:
    """
    None если за последние 30 минут уже получали данные о городе,
    в противном случае возвращаем существующие данные
    """
    weather_data = WeatherData.get_fresh_city(city)
    if weather_data is not None:
        return weather_data

    weather_api_data = get_weather_data_by_city_name(city)

    if weather_api_data is not None:
        return WeatherData.objects.create(
            city=city,
            temp=weather_api_data["fact"]["temp"],
            pressure=weather_api_data["fact"]["pressure_mm"],
            wind=weather_api_data["fact"]["wind_speed"],
        )
