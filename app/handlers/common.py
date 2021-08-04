from aiogram import Dispatcher, types

from app.config_reader import load_config

config = load_config("config/bot.ini")


async def cmd_start(message: types.Message):
    await message.delete()
    await message.answer('''
👋I can convert convert text(ASCII/UTF-8) to binary and vice versa.
❓ /help''')


async def cmd_help(message: types.Message):
    await message.delete()
    await message.answer('''
/binary_to_text - convert binary to text
/text_to_binary - convert text to binary
/cancel - cancel command
/help - print list of commands''')


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_help, commands="help", state="*")
