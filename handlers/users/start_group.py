from aiogram import types
from loader import dp
from filters.groups import IsGroup

@dp.message_handler(IsGroup(),commands=["start", "help"])
async def do_start(message: types.Message):
    await message.reply(f"@{message.from_user.username} <b>Tabriklaymiz🥳🤩</b>\n<i>Siz bu buyruq orqali bizning jamoga qoshildingiz!</i>", parse_mode="html")
