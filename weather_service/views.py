from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import WeatherDataSerializer
from .services import get_or_create_weather_data


class WeatherView(APIView):
    def get(self, request):
        city = request.query_params.get("city")
        if not city:
            return Response(
                {"error": "Обязательный параметр city не передан."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        weather_data = get_or_create_weather_data(city)
        if weather_data is None:
            return Response(
                {
                    "error": "Не удалось получить данные о погоде, проверьте название города на корректность."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = WeatherDataSerializer(weather_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
