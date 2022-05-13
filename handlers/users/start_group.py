from aiogram import types
from loader import dp
from filters.groups import IsGroup

@dp.message_handler(IsGroup(),commands=["start", "help"])
async def do_start(message: types.Message):
    await message.reply(f"{message.from_user.username} <b>Ishing yoqmayo start basishdan bashqa🤣</b>", parse_mode="html")

