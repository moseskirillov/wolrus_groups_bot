from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot.keyboards import add_to_group_keyboard
from bot.keyboards import location_keyboard
from bot.keyboards import mcd_lines_keyboard
from bot.keyboards import mck_stations_keyboard
from bot.keyboards import metro_lines_keyboard
from bot.keyboards import metro_stations_keyboard
from bot.keyboards import mo_cities_keyboard
from bot.keyboards import start_keyboard
from bot.keyboards import transport_types
from bot.titles import MOSCOW_LOCATION_CALLBACK
from bot.titles import MO_LOCATION_CALLBACK
from bot.titles import ONLINE_LOCATION_CALLBACK
from bot.wrappers import callback_answer
from bot.wrappers import check_user_contact
from bot.wrappers import check_user_login
from repositories.groups import select_group_by_id
from repositories.groups import select_groups_by_district
from repositories.groups import select_groups_by_station
from repositories.groups import select_online_groups
from repositories.regional_leaders import get_regional_leader_by_telegram_id
from repositories.requests import create_request
from repositories.users import create_or_update_user
from repositories.users import get_user_by_telegram_id


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            f'Привет, {update.effective_chat.first_name}!\n'
            f'Чтобы найти домашнюю группу,\n'
            f'нажмите на кнопку'
        ),
        reply_markup=start_keyboard,
    )
    context.chat_data['message_id'] = message.id
    context.user_data['user_id'] = update.effective_chat.id
    await create_or_update_user(
        first_name=update.effective_chat.first_name,
        last_name=update.effective_chat.last_name or None,
        telegram_id=str(update.effective_chat.id),
        telegram_login=update.effective_chat.username,
    )


@check_user_login
@callback_answer
async def location_adult_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_id = context.chat_data['message_id']
    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=message_id,
        text='Выберите ваше местонахождение',
        reply_markup=location_keyboard,
    )


@check_user_login
@callback_answer
async def transport_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_id = context.chat_data['message_id']
    callback = update.callback_query.data
    if callback == MOSCOW_LOCATION_CALLBACK:
        keyboard = await transport_types()
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=message_id,
            text='Выберите ближайший транспорт',
            reply_markup=keyboard,
        )
    elif callback == MO_LOCATION_CALLBACK:
        keyboard = await mo_cities_keyboard()
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=message_id,
            text='Выберите город',
            reply_markup=keyboard,
        )
    elif callback == ONLINE_LOCATION_CALLBACK:
        groups = await select_online_groups()
        for group in groups:
            keyboard = add_to_group_keyboard(group.id, group.leader.user.telegram_id)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=(
                    f"Дни проведения: <b>{', '.join(g.title for g in group.days)}</b>\n"
                    f"Время: <b>{group.time.strftime('%H:%M')}</b>\n"
                    f"Возраст: <b>{group.age}</b>\n"
                    f"Тип: <b>{group.type}</b>\n"
                    f"Лидер: <b>{group.leader.user.first_name} "
                    f"{group.leader.user.last_name}</b>\n"
                ),
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard,
            )


@check_user_login
@callback_answer
async def transport_type_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_id = context.chat_data['message_id']
    callback = update.callback_query.data
    match callback:
        case 'metro':
            keyboard = await metro_lines_keyboard(callback)
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=message_id,
                text='Выберите ветку метро',
                reply_markup=keyboard,
            )
        case 'mck':
            keyboard = await mck_stations_keyboard()
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=message_id,
                text='Выберите станцию',
                reply_markup=keyboard,
            )
        case 'mcd':
            keyboard = await mcd_lines_keyboard(callback)
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=message_id,
                text='Выберите диаметр',
                reply_markup=keyboard,
            )


@check_user_login
@callback_answer
async def metro_station_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_id = context.chat_data['message_id']
    callback = update.callback_query.data
    keyboard = await metro_stations_keyboard(callback)
    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=message_id,
        text='Выберите станцию метро',
        reply_markup=keyboard,
    )


@check_user_login
@callback_answer
async def mo_city_groups_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    callback = update.callback_query.data
    groups = await select_groups_by_district(callback)
    await groups_process(context, groups, update)


@check_user_login
@callback_answer
async def groups_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    callback = update.callback_query.data
    groups = await select_groups_by_station(callback)
    await groups_process(context, groups, update)


@check_user_login
@check_user_contact
async def send_request_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    callback = context.chat_data["add_to_group_callback"]
    group_id = callback[0]
    leader_telegram_id = callback[1]
    contact = context.chat_data["contact"]
    message = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Ваш запрос принят, ожидайте'
    )
    group = await select_group_by_id(group_id)
    user_telegram_id = context.user_data.get('user_id')
    user = await get_user_by_telegram_id(str(user_telegram_id))
    regional_leader = await get_regional_leader_by_telegram_id(group.leader.regional_leader_id)
    await create_request(user.id, int(group_id))
    await context.bot.send_message(
        chat_id=leader_telegram_id,
        text="Пришел запрос на добавление в вашу домашнюю группу, данные человека:"
    )
    await context.bot.send_contact(chat_id=leader_telegram_id, contact=contact)
    await context.bot.send_message(
        chat_id=regional_leader.user.telegram_id,
        text='Пришел запрос на добавление в домашнюю группу вашего региона, имя лидера: '
             f'{group.leader.user.first_name} {group.leader.user.last_name}, данные человека:'
    )
    await context.bot.send_contact(chat_id=regional_leader.user.telegram_id, contact=contact)
    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=message.id,
        text='Спасибо, лидер свяжется с вами в ближайшее время'
    )


async def groups_process(context, groups, update):
    for group in groups:
        keyboard = add_to_group_keyboard(group.id, group.leader.user.telegram_id)
        transport_stations = {
            transport: [station.title for station in group.stations if station.transport.title == transport]
            for transport in {s.transport.title for s in group.stations}
        }
        transport_text = "\n".join(
            f"{transport}: <b>{', '.join(stations)}</b>"
            for transport, stations in transport_stations.items()
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                f"{transport_text}\n"
                f"Дни проведения: <b>{', '.join(g.title for g in group.days)}</b>\n"
                f"Время: <b>{group.time.strftime('%H:%M')}</b>\n"
                f"Возраст: <b>{group.age}</b>\n"
                f"Тип: <b>{group.type}</b>\n"
                f"Лидер: <b>{group.leader.user.first_name} "
                f"{group.leader.user.last_name}</b>\n"
            ),
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard,
        )
