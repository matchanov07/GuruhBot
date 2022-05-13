import asyncio
import datetime
import re

import aiogram
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import BadRequest

from filters import IsGroup, AdminFilter
from loader import dp, bot


# /ro oki !ro (read-only) komandalari uchun handler
# foydalanuvchini read-only ya'ni faqat o'qish rejimiga o'tkazib qo'yamiz.
@dp.message_handler(IsGroup(), Command("ro", prefixes="!/"), AdminFilter())
async def read_only_mode(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id
    command_parse = re.compile(r"(!ro|/ro) ?(\d+)? ?([\w+\D]+)?")
    parsed = command_parse.match(message.text)
    time = parsed.group(2)
    comment = parsed.group(3)
    if not time:
        time = 5

    """
    !ro 
    !ro 5 
    !ro 5 test
    !ro test
    !ro test test test
    /ro 
    /ro 5 
    /ro 5 test
    /ro test
    """
    # 5-minutga izohsiz cheklash
    # !ro 5
    # command='!ro' time='5' comment=[]

    # 50 minutga izoh bilan cheklash
    # !ro 50 reklama uchun ban
    # command='!ro' time='50' comment=['reklama', 'uchun', 'ban']

    time = int(time)

    # Ban vaqtini hisoblaymiz (hozirgi vaqt + n minut)
    until_date = datetime.datetime.now() + datetime.timedelta(minutes=time)

    try:
        user_allowed = types.ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_polls=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False,
            can_invite_users=False,
            can_change_info=False,
            can_pin_messages=False,
        )
        # await message.chat.restrict(user_id=member_id, can_send_messages=False, can_send_media_messages=True,  until_date=until_date)
        await bot.restrict_chat_member(chat_id=message.chat.id ,user_id=member_id, permissions=user_allowed, until_date=until_date)
        await message.reply_to_message.delete()
    except aiogram.utils.exceptions.BadRequest as err:
        await message.answer(f"Xatolik! {err.args}")
        return

    if comment is not None:
        await message.answer(f"Foydalanuvchi {message.reply_to_message.from_user.full_name} {time} minut yozish huquqidan mahrum qilindi.\n"
                             f"Sabab: \n<b>{comment}</b>")
    else:
        await message.answer(f"Foydalanuvchi {message.reply_to_message.from_user.full_name} {time} minut yozish huquqidan mahrum qilindi")

    service_message = await message.reply("Xabar 5 sekunddan so'ng o'chib ketadi.")
    # 5 sekun kutib xabarlarni o'chirib tashlaymiz
    await asyncio.sleep(5)
    await message.delete()
    await service_message.delete()

# read-only holatdan qayta tiklaymiz
@dp.message_handler(IsGroup(), Command("unro", prefixes="!/"), AdminFilter())
async def undo_read_only_mode(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id

    user_allowed = types.ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True,
        can_invite_users=True,
        can_change_info=False,
        can_pin_messages=False,
    )
    service_message = await message.reply("Xabar 5 sekunddan so'ng o'chib ketadi.")

    await asyncio.sleep(5)
    await message.chat.restrict(user_id=member_id, permissions=user_allowed, until_date=0)
    await message.reply(f"Foydalanuvchi {member.full_name} tiklandi")

    # xabarlarni o'chiramiz
    await message.delete()
    await service_message.delete()

# Foydalanuvchini banga yuborish (guruhdan haydash)
@dp.message_handler(IsGroup(), Command("ban", prefixes="!/"), AdminFilter())
async def ban_user(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id
    await message.chat.kick(user_id=member_id)

    await message.answer(f"Foydalanuvchi {message.reply_to_message.from_user.full_name} guruhdan haydaldi")
    service_message = await message.reply("Xabar 5 sekunddan so'ng o'chib ketadi.")

    await asyncio.sleep(5)
    await message.delete()
    await service_message.delete()

# Foydalanuvchini bandan chiqarish, foydalanuvchini guruhga qo'sha olmaymiz (o'zi qo'shilishi mumkin)
@dp.message_handler(IsGroup(), Command("unban", prefixes="!/"), AdminFilter())
async def unban_user(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id
    await message.chat.unban(user_id=member_id)
    await message.answer(f"Foydalanuvchi {message.reply_to_message.from_user.full_name} bandan chiqarildi")
    service_message = await message.reply("Xabar 5 sekunddan so'ng o'chib ketadi.")

    await asyncio.sleep(5)

    await message.delete()
    await service_message.delete()  