from django.core.management.base import BaseCommand

from weather_service.weather_bot.bot import main


class Command(BaseCommand):
    help = "Запускает Telegram бота"

    def handle(self, *args, **kwargs):
        main()
