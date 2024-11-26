from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot.keyboards import add_to_group_keyboard
from bot.keyboards import location_adult_keyboard
from bot.keyboards import location_young_keyboard
from bot.keyboards import mcd_lines_keyboard
from bot.keyboards import mck_stations_keyboard
from bot.keyboards import metro_lines_keyboard
from bot.keyboards import metro_stations_keyboard
from bot.keyboards import mo_cities_keyboard
from bot.keyboards import mo_return_keyboard
from bot.keyboards import msk_return_keyboard
from bot.keyboards import online_return_keyboard
from bot.keyboards import start_keyboard
from bot.keyboards import transport_types
from bot.titles import MOSCOW_LOCATION_CALLBACK
from bot.titles import MO_LOCATION_CALLBACK
from bot.titles import ONLINE_LOCATION_CALLBACK
from bot.wrappers import callback_answer, check_user_admin
from bot.wrappers import check_user_contact
from bot.wrappers import check_user_login
from config.settings import settings
from repositories.groups import select_group_by_id
from repositories.groups import select_groups_by_district
from repositories.groups import select_groups_by_station
from repositories.groups import select_online_groups
from repositories.regional_leaders import get_regional_leader_by_telegram_id
from repositories.requests import (
    create_request,
    get_requests,
    get_request_by_id,
    update_request_by_id,
)
from repositories.users import create_or_update_user
from repositories.users import get_user_by_telegram_id


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    is_admin = await create_or_update_user(
        first_name=update.effective_chat.first_name,
        last_name=update.effective_chat.last_name or None,
        telegram_id=str(update.effective_chat.id),
        telegram_login=update.effective_chat.username,
    )
    message_id = context.chat_data.get("message_id")
    context.chat_data["is_admin"] = is_admin
    start_kb = start_keyboard(is_admin)
    if message_id is not None and update.callback_query:
        await update.callback_query.answer()
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=message_id,
            text=(
                f"Привет, {update.effective_chat.first_name}!\n"
                f"Чтобы найти домашнюю группу,\n"
                f"нажмите на кнопку"
            ),
            reply_markup=start_kb,
        )
    else:
        message = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                f"Привет, {update.effective_chat.first_name}!\n"
                f"Чтобы найти домашнюю группу,\n"
                f"нажмите на кнопку"
            ),
            reply_markup=start_kb,
        )
        context.chat_data["message_id"] = message.id
        context.user_data["user_id"] = update.effective_chat.id


@check_user_login
@callback_answer
@check_user_admin
async def requests_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = context.user_data.get("user_id")
    user = await get_user_by_telegram_id(str(user_id))
    requests = await get_requests(user.is_youth_admin)
    for request in requests:
        telegram_text = (
            f"Телеграм: @{request.group.leader.user.telegram_login}\n"
            if not user.is_youth_admin
            else ""
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                f"Заявка в группу лидера\n"
                f"{request.group.leader.user.first_name} "
                f"{request.group.leader.user.last_name}\n"
                f"{telegram_text}"
                f"на {request.date.strftime("%d.%m.%Y")}\nот "
                f"{request.user.last_name} {request.user.first_name}\n"
                f"Телеграм: @{request.user.telegram_login}\n"
                f"Телефон: {request.user.phone}"
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Обработана", callback_data=f"{request.id}_process"
                        )
                    ]
                ]
            ),
        )
    message = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Чтобы вернуться, нажмите на кнопку",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="return_to_start")]]),
    )
    context.chat_data["message_id"] = message.id


@check_user_login
@callback_answer
@check_user_admin
async def requests_process_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request_id = update.callback_query.data.split("_")[0]
    request = await get_request_by_id(request_id)
    if request is not None and request.is_processed == False:
        context.chat_data["request_id"] = request_id
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Напишите комментарий или нажмите кнопку",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Нет комментария",
                            callback_data=f"{request.id}_not_comment",
                        )
                    ]
                ]
            ),
        )
    else:
        start_kb = start_keyboard(True)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Заявка не найдена или уже обработана другим пользователем",
            reply_markup=start_kb,
        )


@check_user_login
@callback_answer
async def close_request_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request_id = context.chat_data.get("request_id")
    start_kb = start_keyboard(True)
    if request_id is not None:
        text = (
            "Нет комментария"
            if update.callback_query
            else update.effective_message.text
        )
        await update_request_by_id(request_id, text)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Заявка успешно обработана",
            reply_markup=start_kb,
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Заявка не найдена или уже обработана другим пользователем",
            reply_markup=start_kb,
        )


@check_user_login
@callback_answer
async def location_adult_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_id = context.chat_data["message_id"]
    context.chat_data["age"] = "adult"
    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=message_id,
        text="Выберите ваше местонахождение",
        reply_markup=location_adult_keyboard,
    )


@check_user_login
@callback_answer
async def location_young_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_id = context.chat_data["message_id"]
    context.chat_data["age"] = "young"
    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=message_id,
        text="Выберите ваше местонахождение",
        reply_markup=location_young_keyboard,
    )


@check_user_login
@callback_answer
async def transport_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_id = context.chat_data["message_id"]
    callback = update.callback_query.data
    age_type = context.chat_data["age"]
    if callback == MOSCOW_LOCATION_CALLBACK or callback == "transport_type_return":
        keyboard = await transport_types(MOSCOW_LOCATION_CALLBACK, age_type)
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=message_id,
            text="Выберите ближайший транспорт",
            reply_markup=keyboard,
        )
    elif callback == MO_LOCATION_CALLBACK:
        keyboard = await mo_cities_keyboard(MO_LOCATION_CALLBACK, age_type)
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=message_id,
            text="Выберите город",
            reply_markup=keyboard,
        )
    elif callback == ONLINE_LOCATION_CALLBACK:
        groups = await select_online_groups(age_type)
        for group in groups:
            keyboard = add_to_group_keyboard(group.id, group.leader.user.telegram_id)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=(
                    f"Дни проведения: <b>{", ".join(g.title for g in group.days)}</b>\n"
                    f"Время: <b>{group.time.strftime("%H:%M")}</b>\n"
                    f"Возраст: <b>{group.age}</b>\n"
                    f"Тип: <b>{group.type}</b>\n"
                    f"Лидер: <b>{group.leader.user.first_name} "
                    f"{group.leader.user.last_name}</b>\n"
                ),
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard,
            )
            message = await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Чтобы вернуться, нажмите на кнопку",
                reply_markup=InlineKeyboardMarkup(online_return_keyboard(age_type)),
            )
            context.chat_data["message_id"] = message.id


@check_user_login
@callback_answer
async def transport_type_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_id = context.chat_data["message_id"]
    callback = update.callback_query.data
    age_type = context.chat_data["age"]
    match callback:
        case "metro":
            keyboard = await metro_lines_keyboard(callback, age_type)
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=message_id,
                text="Выберите ветку метро",
                reply_markup=keyboard,
            )
        case "mck":
            keyboard = await mck_stations_keyboard(callback, age_type)
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=message_id,
                text="Выберите станцию",
                reply_markup=keyboard,
            )
        case "mcd":
            keyboard = await mcd_lines_keyboard(callback, age_type)
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=message_id,
                text="Выберите диаметр",
                reply_markup=keyboard,
            )


@check_user_login
@callback_answer
async def metro_station_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_id = context.chat_data["message_id"]
    callback = update.callback_query.data
    age_type = context.chat_data["age"]
    keyboard = await metro_stations_keyboard(callback, age_type)
    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=message_id,
        text="Выберите станцию метро",
        reply_markup=keyboard,
    )


@check_user_login
@callback_answer
async def mo_city_groups_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    callback = update.callback_query.data
    age_type = context.chat_data["age"]
    groups = await select_groups_by_district(callback, age_type)
    await groups_process(context, groups, update)
    message = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Чтобы вернуться, нажмите на кнопку",
        reply_markup=mo_return_keyboard,
    )
    context.chat_data["message_id"] = message.id


@check_user_login
@callback_answer
async def groups_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    callback = update.callback_query.data
    age_type = context.chat_data["age"]
    groups = await select_groups_by_station(callback, age_type)
    await groups_process(context, groups, update)
    message = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Чтобы вернуться, нажмите на кнопку",
        reply_markup=msk_return_keyboard,
    )
    context.chat_data["message_id"] = message.id


@check_user_login
@check_user_contact
async def send_request_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    callback = context.chat_data["add_to_group_callback"]
    group_id = callback[0]
    leader_telegram_id = callback[1]
    age_type = context.chat_data["age"]
    contact = context.chat_data["contact"]
    message = await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Ваш запрос принят, ожидайте"
    )
    group = await select_group_by_id(group_id)
    user_telegram_id = context.user_data.get("user_id")
    user = await get_user_by_telegram_id(str(user_telegram_id))
    await create_request(user.id, int(group_id))
    if age_type == "adult":
        regional_leader = await get_regional_leader_by_telegram_id(
            group.leader.regional_leader_id
        )
        await context.bot.send_message(
            chat_id=leader_telegram_id,
            text="Пришел запрос на добавление в вашу домашнюю группу, данные человека:",
        )
        await context.bot.send_contact(chat_id=leader_telegram_id, contact=contact)
        await context.bot.send_message(
            chat_id=regional_leader.user.telegram_id,
            text="Пришел запрос на добавление в домашнюю группу вашего региона, имя лидера: "
            f"{group.leader.user.first_name} {group.leader.user.last_name}, данные человека:",
        )
        await context.bot.send_contact(
            chat_id=regional_leader.user.telegram_id, contact=contact
        )
    else:
        leader_telegram_id = settings.bot.young_admin_id
        await context.bot.send_message(
            chat_id=leader_telegram_id,
            text=f"Пришел запрос на добавление в домашнюю группу, имя лидера "
            f"{group.leader.user.first_name} "
            f"{group.leader.user.last_name}, данные человека:",
        )
        await context.bot.send_contact(chat_id=leader_telegram_id, contact=contact)
    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=message.id,
        text="Спасибо, лидер свяжется с вами в ближайшее время",
    )


async def groups_process(context, groups, update):
    for group in groups:
        keyboard = add_to_group_keyboard(group.id, group.leader.user.telegram_id)
        transport_stations = {
            transport: [
                station.title
                for station in group.stations
                if station.transport.title == transport
            ]
            for transport in {s.transport.title for s in group.stations}
        }
        transport_text = "\n".join(
            f"{transport}: <b>{", ".join(stations)}</b>"
            for transport, stations in transport_stations.items()
        )
        description = f"{group.description if group.description else ""}\n"
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                f"{transport_text}\n"
                f"Район: <b>{group.district.title}</b>\n"
                f"Дни проведения: <b>{", ".join(g.title for g in group.days)}</b>\n"
                f"Время: <b>{group.time.strftime("%H:%M")}</b>\n"
                f"Возраст: <b>{group.age}</b>\n"
                f"Тип: <b>{group.type}</b>\n"
                f"Лидер: <b>{group.leader.user.first_name} "
                f"{group.leader.user.last_name}</b>\n"
                f"{"Примечание " if description != "" else ""}{description}"
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard,
        )
