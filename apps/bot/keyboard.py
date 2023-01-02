from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegram_bot_pagination import InlineKeyboardPaginator

def start_command():
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="Создать пост", callback_data="create_post"),
        InlineKeyboardButton(text="Мои посты", callback_data="get_post"),
        InlineKeyboardButton(text="Удалить пост", callback_data="delete_post"),
    )
    return keyboard