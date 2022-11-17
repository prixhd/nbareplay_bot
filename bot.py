
import json
from aiogram.types import InlineKeyboardMarkup
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Text
from config_reader import config

bot = Bot(token=config.bot_token.get_secret_value())

dp = Dispatcher(bot)

with open("matchs_dict.json") as file:
    matchs_dict = json.load(file)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Получить матчи за сегодня"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Запись матчей NBA", reply_markup=keyboard)


@dp.message_handler(Text(equals="Получить матчи за сегодня"))
async def matchs_today(message: types.Message):
    matchs_buttons = []
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for k, v in matchs_dict.items():
        title = f"{v['match_title']}"
        matchs_buttons.append(title)

    keyboard.add(*matchs_buttons)
    await message.answer("Выберите матч для просмотра", reply_markup=keyboard)


for a, b in sorted(matchs_dict.items()):
    @dp.message_handler(Text(equals={b['match_title']}))
    async def match_answer(message: types.Message):
        builder = InlineKeyboardMarkup()
        builder.row(types.InlineKeyboardButton(
            text='Первая четверть', url=b['first_quarter'])
        )
        builder.row(types.InlineKeyboardButton(
            text='Вторая четверть', url=b['second_quarter'])
        )
        builder.row(types.InlineKeyboardButton(
            text='Третья четверть', url=b['third_quarter'])
        )
        builder.row(types.InlineKeyboardButton(
            text='Четвертая четверть', url=b['fourth_quarter'])
        )
        await message.answer('Выберите четверть', reply_markup=builder)


if __name__ == "__main__":
    executor.start_polling(dp)
