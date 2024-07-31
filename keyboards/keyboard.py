from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.database import users

def edit_keyboard(reminders: dict) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for number, reminder in sorted(reminders.items()):
        kb.row(InlineKeyboardButton(
            text=f'❌{number} - {reminder}', callback_data=f'{number}del'
        ))
    return kb.as_markup()



