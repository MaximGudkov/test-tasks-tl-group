from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from weather_service.models import WeatherData


class WeatherViewTests(APITestCase):
    def test_missing_city_parameter(self):
        url = reverse("weather:weather_api")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {"error": "Обязательный параметр city не передан."}
        )

    @patch("weather_service.services.get_or_create_weather_data")
    def test_invalid_city(self, mock_get_or_create_weather_data):
        mock_get_or_create_weather_data.return_value = None
        url = reverse("weather:weather_api")
        response = self.client.get(url, {"city": "InvalidCity"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {
                "error": "Не удалось получить данные о погоде или определить координаты города."
            },
        )

    @patch("weather_service.services.get_or_create_weather_data")
    def test_valid_city(self, mock_get_or_create_weather_data):
        weather_data = WeatherData(city="Москва", temp=25, pressure=1012, wind=5)
        mock_get_or_create_weather_data.return_value = weather_data

        url = reverse("weather:weather_api")
        response = self.client.get(url, {"city": "Москва"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_keys = ["city", "temp", "pressure", "wind"]
        for key in expected_keys:
            self.assertIn(key, response.data)

    @patch("weather_service.services.get_or_create_weather_data")
    def test_request_throughout_30_minutes_for_same_city_returns_same_data(self, mock_get_or_create_weather_data):
        first_weather_data = WeatherData(city="Москва", temp=25, pressure=1012, wind=5)
        second_weather_data = WeatherData(city="Москва", temp=20, pressure=1000, wind=3)

        mock_get_or_create_weather_data.side_effect = [first_weather_data, second_weather_data]

        url = reverse("weather:weather_api")

        first_response = self.client.get(url, {"city": "Москва"})
        self.assertEqual(first_response.status_code, status.HTTP_200_OK)
        first_response_data = first_response.data

        second_response = self.client.get(url, {"city": "Москва"})
        self.assertEqual(second_response.status_code, status.HTTP_200_OK)
        second_response_data = second_response.data

        self.assertEqual(first_response_data, second_response_data)
