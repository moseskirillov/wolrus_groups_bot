from functools import wraps

from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import ContextTypes

from repositories.users import update_user_phone


def check_user_login(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = context.user_data.get("user_id")
        message_id = context.chat_data.get("message_id")
        if update.callback_query:
            await update.callback_query.answer()
        if user_id and message_id:
            return await func(update, context)
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Вы не залогинены. Для логина, сначала нажмите /start"
            )

    return wrapper


def callback_answer(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.callback_query:
            await update.callback_query.answer()
        await func(update, context)

    return wrapper


def check_user_contact(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        callback = (
            update.callback_query.data.replace("add_to_group_", "").split("_")
            if update.callback_query and update.callback_query.data
            else context.chat_data["add_to_group_callback"]
        )
        context.chat_data["add_to_group_callback"] = callback
        contact = (
            update.message.contact
            if update.message and update.message.contact
            else context.chat_data["contact"]
            if context.chat_data.get("contact")
            else None
        )
        context.chat_data["contact"] = contact
        if update.callback_query:
            await update.callback_query.answer()
        if contact is None:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Нажмите на кнопку чтобы отправить Ваш контакт и лидер мог связаться с вами",
                reply_markup=ReplyKeyboardMarkup(
                    [
                        [KeyboardButton(text="Отправить контакт", request_contact=True)]
                    ],
                    one_time_keyboard=True,
                    resize_keyboard=True
                )
            )
        else:
            await update_user_phone(str(update.effective_chat.id), contact.phone_number)
            await func(update, context)

    return wrapper
