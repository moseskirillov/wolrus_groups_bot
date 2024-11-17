import re

from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

from bot.titles import ADULT_BUTTON_TITLE
from bot.titles import MOSCOW_BUTTON_TITLE
from bot.titles import MOSCOW_LOCATION_CALLBACK
from bot.titles import MO_BUTTON_TITLE
from bot.titles import MO_LOCATION_CALLBACK
from bot.titles import ONLINE_BUTTON_TITLE
from bot.titles import ONLINE_LOCATION_CALLBACK
from bot.titles import RETURN_BUTTON_TITLE
from bot.titles import RETURN_TO_AGE_CALLBACK
from bot.titles import START_SEARCH_ADULT_CALLBACK
from bot.titles import START_SEARCH_YOUNG_CALLBACK
from bot.titles import YOUNG_BUTTON_TITLE
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

location_adult_keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(MOSCOW_BUTTON_TITLE, callback_data=MOSCOW_LOCATION_CALLBACK)],
        [InlineKeyboardButton(MO_BUTTON_TITLE, callback_data=MO_LOCATION_CALLBACK)],
        [InlineKeyboardButton(ONLINE_BUTTON_TITLE, callback_data=ONLINE_LOCATION_CALLBACK)],
        [InlineKeyboardButton(RETURN_BUTTON_TITLE, callback_data=RETURN_TO_AGE_CALLBACK)],
    ]
)

location_young_keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(MOSCOW_BUTTON_TITLE, callback_data=MOSCOW_LOCATION_CALLBACK)],
        [InlineKeyboardButton(ONLINE_BUTTON_TITLE, callback_data=ONLINE_LOCATION_CALLBACK)],
        [InlineKeyboardButton(RETURN_BUTTON_TITLE, callback_data=RETURN_TO_AGE_CALLBACK)],
    ]
)

msk_return_keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Назад", callback_data="transport_type_return")],
        [InlineKeyboardButton("В начало", callback_data="return_to_start")],
    ]
)

mo_return_keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Назад", callback_data=MO_LOCATION_CALLBACK)],
        [InlineKeyboardButton("В начало", callback_data="return_to_start")],
    ]
)


def online_return_keyboard(age_type):
    return [
        [InlineKeyboardButton("Назад", callback_data="start_search_adult" if age_type == "adult" else "start_search_young")],
        [InlineKeyboardButton("В начало", callback_data="return_to_start")],
    ]


def add_to_group_keyboard(group_id, leader_telegram_id):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Присоединиться",
                    callback_data=f"add_to_group_{group_id}_{leader_telegram_id}",
                )
            ]
        ]
    )


async def transport_types(callback, age_group, age_types):
    types = await select_moscow_transports(age_group, age_types)
    keyboard = split_list_and_create_buttons(types, callback, age_group)
    return keyboard


async def metro_lines_keyboard(callback, age_group):
    lines = await select_available_metro_lines(callback, age_group)
    keyboard = split_list_and_create_buttons(lines, callback)
    return keyboard


async def mcd_lines_keyboard(callback, age_group):
    lines = await select_available_metro_lines(callback, age_group)
    keyboard = split_list_and_create_buttons(lines, callback)
    return keyboard


async def metro_stations_keyboard(callback, age_group):
    stations = await select_stations_by_line(callback, age_group)
    return split_list_and_create_buttons(stations, callback)


async def mck_stations_keyboard(callback, age_group):
    stations = await select_stations_by_mck(age_group)
    return split_list_and_create_buttons(stations, callback)


async def mo_cities_keyboard(callback):
    cities = await select_mo_districts()
    return split_list_and_create_buttons(cities, callback)


def split_list_and_create_buttons(input_list, callback=None, age_group=None):
    def create_button(item):
        return InlineKeyboardButton(
            text=item.color if hasattr(item, "color") else item.title,
            callback_data=item.callback_data,
        )

    sub_lists = [input_list[i: i + 2] for i in range(0, len(input_list), 2)]
    inline_keyboard = []
    for sublist in sub_lists:
        buttons = [create_button(item) for item in sublist]
        inline_keyboard.append(buttons)
    return_button = add_return_button(callback, age_group)
    if return_button:
        inline_keyboard.append(return_button)
    return InlineKeyboardMarkup(inline_keyboard)


def add_return_button(callback, age_group=None):
    if callback in ["moscow", "mo"]:
        if age_group and age_group == "adult":
            return [InlineKeyboardButton(text=RETURN_BUTTON_TITLE, callback_data="location_return")]
        else:
            return [InlineKeyboardButton(text=RETURN_BUTTON_TITLE, callback_data="start_search_young")]
    elif callback in ["metro", "mck", "mcd"]:
        return [InlineKeyboardButton(text=RETURN_BUTTON_TITLE, callback_data="transport_type_return")]
    elif re.match(r'\w+_line_callback', callback):
        return [InlineKeyboardButton(text=RETURN_BUTTON_TITLE, callback_data="transport_type_return")]
    else:
        return None
