import binascii

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup

from app.config_reader import load_config

config = load_config("config/bot.ini")
bot = Bot(token=config.bot.TOKEN)


class TextToBinary(StatesGroup):
    start = State()
    waiting_for_text = State()


def text_binary(text):
    line = binary = ''
    text = text.encode('utf-8')
    j, m = divmod(len(text), 16)
    generator = []
    for i in range(j):
        generator.append(text[i * 16:(i + 1) * 16])
    if m:
        generator.append(text[j * 16:])
    #
    for add_r, d in enumerate(generator):
        hex_str = binascii.hexlify(d)
        hex_str = hex_str.decode('ascii')
        j, m = divmod(len(hex_str.upper()), 2)
        generator = []
        for i in range(j):
            generator.append(hex_str.upper()[i * 2:(i + 1) * 2])
        dump_str = ' '.join(generator)
        line += dump_str[:8 * 3]
        if len(d) > 8:
            line += ' ' + dump_str[8 * 3:]
        line += ' '
    hex_list = [t for t in line.split(' ') if t != '']
    for h in hex_list:
        binary += bin(int(h, 16))[2::] + ' '
    return binary[0:-1]


async def cmd_text_to_binary(message: types.Message):
    await message.delete()
    await message.answer('Enter text:')
    await TextToBinary.waiting_for_text.set()


async def entering_text(message: types.Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    await message.delete()
    if message.text != '/cancel':
        await message.answer(text_binary(message.text))
    else:
        await message.answer('Successfully')
    await TextToBinary.first()


def register_text_to_binary(dp: Dispatcher):
    dp.register_message_handler(cmd_text_to_binary, commands="text_to_binary", state="*")
    dp.register_message_handler(entering_text, state=TextToBinary.waiting_for_text)
