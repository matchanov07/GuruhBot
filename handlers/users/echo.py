from aiogram import types
from filters.private import IsPrivate
from loader import dp


# Echo bot
@dp.message_handler( IsPrivate() ,state=None)
async def bot_echo(message: types.Message):
    await message.answer(message.text)
