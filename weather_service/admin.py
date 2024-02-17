from django.contrib import admin

from . import models


@admin.register(models.WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ("city", "last_request")
