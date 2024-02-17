from django.urls import path

from .views import WeatherView

app_name = "weather_service"

urlpatterns = [
    path("weather/", WeatherView.as_view(), name="weather_api"),
]
