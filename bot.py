import json

import aiogram
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Text
from config_reader import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

bot = Bot(token=config.bot_token.get_secret_value())

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

with open("matchs_dict.json") as file:
    matchs_dict = json.load(file)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Получить матчи за сегодня"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Запись матчей NBA", reply_markup=keyboard)


@dp.message_handler(Text(equals="Получить матчи за сегодня"))
async def matchs_today(message: types.Message):
    matchs_buttons = []
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    for k, v in matchs_dict.items():
        title = f"{v['match_title']}({k})"
        matchs_buttons.append(title)

    keyboard.add(*matchs_buttons)
    await message.answer("Выберите матч для просмотра", reply_markup=keyboard)


@dp.message_handler()
async def match_answer(message: types.Message):
    builder = InlineKeyboardMarkup()

    for i in range(1, 5):
        try:
            try:
                builder.add(InlineKeyboardButton(text=f'Четверть №{i}', url=matchs_dict[message.text[-6:-1]][f'Part{i}']))
            except KeyError:
                print(0)
        except aiogram.utils.exceptions.BadRequest:
            print(0)

            # builder.add(InlineKeyboardButton(text=f'Четверть №{i} не вышла'))

    await message.answer('Выберите четверть', reply_markup=builder)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
