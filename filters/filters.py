from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from database.database import users, user_db

class IsDelRemindCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.endswith('del')
