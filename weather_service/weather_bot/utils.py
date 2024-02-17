from weather_service.api_services import get_weather_data_by_city_name


def translate_part_name(part_name: str) -> str:
    parts_translation = {
        "morning": "Утро",
        "day": "День",
        "evening": "Вечер",
        "night": "Ночь",
    }
    return parts_translation.get(part_name, part_name)


def get_weather_forecast(city_name: str) -> str:
    forecast_api_data = get_weather_data_by_city_name(city_name)
    if forecast_api_data is None:
        return "Не удалось получить данные о таком городе"

    today_forecast = forecast_api_data["forecasts"][0]
    parts = today_forecast["parts"]

    forecast_str = f"Погода в {city_name}:\n"
    for part_name, part_data in parts.items():
        if part_name in ("morning", "day", "evening", "night"):
            temp_min = part_data.get("temp_min")
            temp_max = part_data.get("temp_max")
            part_name_rus = translate_part_name(part_name)
            forecast_str += f"{part_name_rus}: мин {temp_min}°C, макс {temp_max}°C\n"
    return forecast_str
