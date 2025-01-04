from telegram.ext import Application
from telegram.ext import ApplicationBuilder
from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import filters

from bot.handlers import (
    feedback_process,
    groups_handler,
    requests_handler,
    requests_process_handler,
    close_request_handler,
)
from bot.handlers import location_adult_handler
from bot.handlers import location_young_handler
from bot.handlers import metro_station_handler
from bot.handlers import mo_city_groups_handler
from bot.handlers import send_request_handler
from bot.handlers import start_handler
from bot.handlers import transport_handler
from bot.handlers import transport_type_handler
from bot.titles import MCD_CALLBACK
from bot.titles import MCK_CALLBACK
from bot.titles import METRO_CALLBACK
from bot.titles import MOSCOW_LOCATION_CALLBACK
from bot.titles import MO_LOCATION_CALLBACK
from bot.titles import ONLINE_LOCATION_CALLBACK
from bot.titles import RETURN_TO_AGE_CALLBACK
from bot.titles import START_COMMAND
from bot.titles import START_SEARCH_ADULT_CALLBACK
from config import init
from config.settings import settings


def handlers_register(bot: Application):
    bot.add_handler(CommandHandler(START_COMMAND, start_handler))
    bot.add_handler(CallbackQueryHandler(start_handler, RETURN_TO_AGE_CALLBACK))
    bot.add_handler(CallbackQueryHandler(requests_handler, "requests_callback"))
    bot.add_handler(CallbackQueryHandler(start_handler, "return_to_start"))
    bot.add_handler(
        CallbackQueryHandler(location_adult_handler, START_SEARCH_ADULT_CALLBACK)
    )
    bot.add_handler(CallbackQueryHandler(location_adult_handler, "location_return"))
    bot.add_handler(CallbackQueryHandler(location_adult_handler, "start_search_adult"))
    bot.add_handler(CallbackQueryHandler(location_young_handler, "start_search_young"))
    bot.add_handler(CallbackQueryHandler(transport_handler, MOSCOW_LOCATION_CALLBACK))
    bot.add_handler(CallbackQueryHandler(transport_handler, MO_LOCATION_CALLBACK))
    bot.add_handler(CallbackQueryHandler(transport_handler, ONLINE_LOCATION_CALLBACK))
    bot.add_handler(CallbackQueryHandler(transport_handler, "transport_type_return"))
    bot.add_handler(CallbackQueryHandler(transport_type_handler, METRO_CALLBACK))
    bot.add_handler(CallbackQueryHandler(transport_type_handler, MCK_CALLBACK))
    bot.add_handler(CallbackQueryHandler(transport_type_handler, MCD_CALLBACK))
    bot.add_handler(CallbackQueryHandler(metro_station_handler, r"\w+_line_callback"))
    bot.add_handler(CallbackQueryHandler(mo_city_groups_handler, "mo_cities_return"))
    bot.add_handler(CallbackQueryHandler(mo_city_groups_handler, r"\w+_mo_city"))
    bot.add_handler(CallbackQueryHandler(groups_handler, r"\w+_station_callback"))
    bot.add_handler(CallbackQueryHandler(requests_process_handler, r"\w+_process"))
    bot.add_handler(CallbackQueryHandler(close_request_handler, r"\w+_not_comment"))
    bot.add_handler(MessageHandler(filters.TEXT, close_request_handler))
    bot.add_handler(CallbackQueryHandler(send_request_handler, r"add_to_group_"))
    bot.add_handler(CallbackQueryHandler(feedback_process, r"\w+_\w+_request_\w+"))
    bot.add_handler(MessageHandler(filters.CONTACT, send_request_handler))


def main():
    init.log_config()
    bot = ApplicationBuilder().token(settings.bot.token).build()
    handlers_register(bot)
    bot.run_webhook(
        listen="0.0.0.0",
        port=3002,
        url_path="",
        webhook_url="https://shgbot.wolrus.org",
    )


if __name__ == "__main__":
    main()
