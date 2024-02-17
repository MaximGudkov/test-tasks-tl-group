from datetime import datetime, timedelta
from typing import Optional

from django.db import models


class WeatherData(models.Model):
    city = models.CharField(max_length=255)
    temp = models.IntegerField()
    pressure = models.IntegerField()
    wind = models.FloatField()
    last_request = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    @classmethod
    def get_fresh_city(cls, city: str) -> Optional["WeatherData"]:
        recent_time_limit = datetime.now() - timedelta(minutes=30)
        same_city_data = cls.objects.filter(
            city=city, last_request__gte=recent_time_limit
        )
        if same_city_data.exists():
            return same_city_data.last()
        return None
