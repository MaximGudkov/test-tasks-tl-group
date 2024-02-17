import logging

from django.conf import settings
from telegram import Update
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          ConversationHandler, MessageHandler, filters)

from weather_service.weather_bot.utils import get_weather_forecast

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

ASKING_FOR_CITY = 0


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Используйте команду /weather чтобы узнать погоду."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "/start - начать работу с ботом\n"
        "/help - показать это сообщение\n"
        "/weather - узнать погоду в указанном городе"
    )


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Введите название города на русском:")
    return ASKING_FOR_CITY


async def ask_for_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    city_name = update.message.text
    weather_info = get_weather_forecast(city_name)
    await update.message.reply_text(weather_info)
    return ConversationHandler.END


def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)


def main() -> None:
    logger.info("Конфигурация бота погоды...")
    logger.info("Проверяющему разработчику большой привет и хорошего рабочего дня! :)")

    application = Application.builder().token(settings.WEATHER_BOT_API_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("weather", weather)],
        states={
            ASKING_FOR_CITY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ask_for_city)
            ],
        },
        fallbacks=[
            CommandHandler("start", start),
            CommandHandler("help", help_command),
        ],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_error_handler(error_handler)

    logger.info("Запуск бота погоды...")
    application.run_polling()
