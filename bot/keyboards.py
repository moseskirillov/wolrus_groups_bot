from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

from bot.titles import MCD_BUTTON_TITLE
from bot.titles import START_SEARCH_YOUNG_CALLBACK
from bot.titles import ADULT_BUTTON_TITLE
from bot.titles import MCD_CALLBACK
from bot.titles import MCK_BUTTON_TITLE
from bot.titles import MCK_CALLBACK
from bot.titles import METRO_BUTTON_TITLE
from bot.titles import METRO_CALLBACK
from bot.titles import MOSCOW_BUTTON_TITLE
from bot.titles import MOSCOW_LOCATION_CALLBACK
from bot.titles import MO_BUTTON_TITLE
from bot.titles import MO_LOCATION_CALLBACK
from bot.titles import ONLINE_BUTTON_TITLE
from bot.titles import ONLINE_LOCATION_CALLBACK
from bot.titles import YOUNG_BUTTON_TITLE
from bot.titles import START_SEARCH_ADULT_CALLBACK
from repositories.districts import select_mo_districts
from repositories.lines import select_available_metro_lines
from repositories.stations import select_stations_by_line
from repositories.stations import select_stations_by_mck
from repositories.transports import select_moscow_transports

start_keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(ADULT_BUTTON_TITLE, callback_data=START_SEARCH_ADULT_CALLBACK)],
        [InlineKeyboardButton(YOUNG_BUTTON_TITLE, callback_data=START_SEARCH_YOUNG_CALLBACK)]
    ]
)

location_keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(MOSCOW_BUTTON_TITLE, callback_data=MOSCOW_LOCATION_CALLBACK)],
        [InlineKeyboardButton(MO_BUTTON_TITLE, callback_data=MO_LOCATION_CALLBACK)],
        [InlineKeyboardButton(ONLINE_BUTTON_TITLE, callback_data=ONLINE_LOCATION_CALLBACK)],
    ]
)

msc_transport_type_keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(METRO_BUTTON_TITLE, callback_data=METRO_CALLBACK)],
        [InlineKeyboardButton(MCK_BUTTON_TITLE, callback_data=MCK_CALLBACK)],
        [InlineKeyboardButton(MCD_BUTTON_TITLE, callback_data=MCD_CALLBACK)],
    ]
)


def add_to_group_keyboard(group_id, leader_telegram_id):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text='Присоединиться',
                    callback_data=f'add_to_group_{group_id}_{leader_telegram_id}',
                )
            ]
        ]
    )


async def transport_types():
    types = await select_moscow_transports()
    keyboard = split_list_and_create_buttons(types)
    return keyboard


async def metro_lines_keyboard(transport_type):
    lines = await select_available_metro_lines(transport_type)
    keyboard = split_list_and_create_buttons(lines)
    return keyboard


async def mcd_lines_keyboard(transport_type):
    lines = await select_available_metro_lines(transport_type)
    keyboard = split_list_and_create_buttons(lines)
    return keyboard


async def metro_stations_keyboard(callback):
    stations = await select_stations_by_line(callback)
    return split_list_and_create_buttons(stations)


async def mck_stations_keyboard():
    stations = await select_stations_by_mck()
    return split_list_and_create_buttons(stations)


async def mo_cities_keyboard():
    cities = await select_mo_districts()
    return split_list_and_create_buttons(cities)


def split_list_and_create_buttons(input_list):
    def create_button(item):
        return InlineKeyboardButton(
            text=item.color if hasattr(item, 'color') else item.title,
            callback_data=item.callback_data,
        )

    sub_lists = [input_list[i: i + 2] for i in range(0, len(input_list), 2)]
    inline_keyboard = []
    for sublist in sub_lists:
        buttons = [create_button(item) for item in sublist]
        inline_keyboard.append(buttons)
    return InlineKeyboardMarkup(inline_keyboard)
