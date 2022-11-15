import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from config_reader import config

bot = Bot(token=config.bot_token.get_secret_value())

