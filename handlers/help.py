from aiogram import types




async def help_command(message: types.Message):
    welcome_text = "Assalomu alaykum siz /help kamandasini yozdingiz"
    await message.answer(welcome_text)
