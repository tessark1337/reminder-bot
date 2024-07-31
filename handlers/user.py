import asyncio
import datetime
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext

from other_functions.markers import normalize_message
from database.database import users, user_db
from filters.filters import IsDelRemindCallbackData
from keyboards.keyboard import edit_keyboard
from FSM import fsm
from lexicon.lexicon import LEXICON_RU

router = Router()
scheduler = AsyncIOScheduler()

async def send_reminder(message: Message, text):
    await message.answer(text)

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(LEXICON_RU['/start'])
    if not users:
        users[message.from_user.id] = user_db

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(LEXICON_RU['/help'])


@router.message(StateFilter(None), Command('set'))
async def set_cmd(message: Message, state: FSMContext):
    await message.answer(LEXICON_RU['set_form'])
    await state.set_state(fsm.SetEvent.form)

@router.message(fsm.SetEvent.form)
async def correctly_set(message: Message, state: FSMContext):
    event = normalize_message(message.text)
    if not event:
        await message.answer(LEXICON_RU['not_data'])
    else:
        await state.update_data(form=event)
        data = await state.get_data()
        info = data['form']

        # Максимальное количество напоминаний
        max_reminders = 30

        # Получить текущее количество напоминаний для пользователя
        current_reminders = len(users[message.from_user.id]['text'])

        if not(datetime.datetime.now().day > int(info['number']) and datetime.datetime.now().month <= int(info['month'])):
            if current_reminders < max_reminders:
                # Увеличить ключ для нового напоминания
                new_key = current_reminders + 1
                users[message.from_user.id]['text'][new_key] = f'{info["number"]} {info["month_name"]} {info["text"]}'
                await message.answer(
                    f'<b>Хорошо, я напомню вам {info["number"]} {info["month_name"]} {info["year"]}г. в {info["time"]}</b> ⏰✅\n\n'
                    f'<em>Текст сообщения</em>: <b>{info["text"]}</b>')
                print(info)
                print(users[message.from_user.id]['text'])
                trigger_time = datetime.datetime(year=int(info["year"]),
                                             month=int(info["month"]),
                                             day=int(info["number"]),
                                             hour=int(info["time"].split(':')[0]),
                                             minute=int(info["time"].split(':')[1]))

                scheduler.add_job(func=send_reminder, trigger=DateTrigger(run_date=trigger_time),
                              args=[message, f'<b>⏰Напоминаю, сейчас вы должны: </b>\n<em>{info["text"]}</em>'])
                scheduler.start()
            else:
               await message.answer(LEXICON_RU['max_reminders_exceeded'])  # Сообщение о превышении лимита
        else:
            await message.answer(LEXICON_RU['event_passed'])
    await state.clear()


@router.message(fsm.SetEvent.form)
async def incorrectly_set(message: Message, state: FSMContext):
    await message.answer(LEXICON_RU['set_incorrectly'])

@router.message(Command('edit'))
async def edit_cmd(message: Message):
    await message.answer(LEXICON_RU['/edit'],
                         reply_markup=edit_keyboard(reminders=users[message.from_user.id]['text']))

@router.callback_query(IsDelRemindCallbackData())
async def del_remind(callback: CallbackQuery):
    del users[callback.from_user.id]['text'][int(callback.data[:-3])]
    await callback.message.edit_text(
        text=LEXICON_RU['/edit'],
        reply_markup=edit_keyboard(
            reminders=users[callback.from_user.id]['text']
        )
    )

