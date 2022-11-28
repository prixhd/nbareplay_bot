import json
import re

import aiogram
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Text

from config_reader import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from pars_nbareplayhd import main
import pars_nbareplayhd_async
from pars_aanba import get_video_rus
from pars_aanba_vk import main

bot = Bot(token=config.bot_token.get_secret_value())

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Получить матчи на англ.яз.", "Получить матчи на русском"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Запись матчей NBA", reply_markup=keyboard)


@dp.message_handler(Text(equals="Получить матчи на русском"))
async def matchs_today(message: types.Message):
    msg = await message.answer("Идет поиск матчей за сегодня..." + "\n\nЭто может занять до 60 сек")

    links = main()
    # links = get_video_rus("https://aanba.ru/zapisi-matchej")

    await msg.delete()

    with open("data/matchs_dict_aanba_vk.json", encoding="utf-8") as file:
        matchs_dict = json.load(file)

    matchs_buttons = []
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    for k, v in matchs_dict.items():
        title = f"{v['match_title']}({k})"
        matchs_buttons.append(title)
    matchs_buttons.append('Назад')
    keyboard.add(*matchs_buttons)
    await message.answer("Выберите матч для просмотра", reply_markup=keyboard)


@dp.message_handler(Text(equals="Получить матчи на англ.яз."))
async def matchs_today(message: types.Message):
    msg = await message.answer("Идет поиск матчей за сегодня..." + "\n\nЭто может занять до 60 сек")

    # links = main()
    await pars_nbareplayhd_async.get_matchs()

    await msg.delete()

    with open("data/matchs_dict.json") as file:
        matchs_dict = json.load(file)

    matchs_buttons = []
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    for k, v in matchs_dict.items():
        title = f"{v['match_title']}({k})"
        matchs_buttons.append(title)
    matchs_buttons.append('Назад')
    keyboard.add(*matchs_buttons)
    await message.answer("Выберите матч для просмотра", reply_markup=keyboard)


@dp.message_handler()
async def match_answer(message: types.Message):
    if '/' not in message.text:
        with open("data/matchs_dict.json") as file:
            matchs_dict = json.load(file)

        builder = InlineKeyboardMarkup(row_width=4)

        for i in range(1, 5):
            try:
                try:
                    builder.add(
                        InlineKeyboardButton(text=f'Четверть №{i}', url=matchs_dict[message.text[-6:-1]][f'Part{i}']))
                except KeyError:
                    # builder.add(InlineKeyboardButton(text=f'Четверть №{i} не вышла'))
                    print(0)
            except aiogram.utils.exceptions.BadRequest:
                print(0)

        await message.answer('Выберите четверть', reply_markup=builder)
    else:
        with open("data/matchs_dict_aanba_vk.json", encoding="utf-8") as file:
            matchs_dict = json.load(file)

        builder = InlineKeyboardMarkup(row_width=4)
        builder.add(InlineKeyboardButton(text=f'Полный матч', url=matchs_dict[message.text[-11:-1]]['full_game']))

        await message.answer('Получите, распишитесь', reply_markup=builder)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
