from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup

from app.config_reader import load_config

config = load_config("config/bot.ini")
bot = Bot(token=config.bot.TOKEN)


class BinaryToText(StatesGroup):
    start = State()
    waiting_for_binary = State()


def binary_text(binary):
    hex_ = ''
    binary = binary.split(' ')
    for x in binary:
        hex_ += '0' * (2 - len(hex(int(x, 2))[2::])) + hex(int(x, 2))[2::] + ' '
    result = bytes()
    text = hex_[0:-1].strip()
    for line in text.split('\n'):
        try:
            result += bytes.fromhex(line)
        except ValueError:
            return '❗️Error: non-binary number found. Words must be 8 numbers length. Please try again '
    return result.decode('utf-8')


async def cmd_binary_to_text(message: types.Message):
    await message.delete()
    await message.answer('Enter binary (######## ######## ########):')
    await BinaryToText.waiting_for_binary.set()


async def entering_binary(message: types.Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    await message.delete()
    if message.text != '/cancel':
        await message.answer(binary_text(message.text))
    else:
        await message.answer('Successfully')
    await BinaryToText.first()


def register_binary_to_text(dp: Dispatcher):
    dp.register_message_handler(cmd_binary_to_text, commands="binary_to_text", state="*")
    dp.register_message_handler(entering_binary, state=BinaryToText.waiting_for_binary)
