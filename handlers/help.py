from aiogram import types




async def help_command(message: types.Message):
    welcome_text = "<b>Assalomu alaykum siz /help kamandasini yozdingiz</b>\n\n<i>Agar botda qandaydir muammolar yuzaga kelgan bo'lsa iltimos adminga murojat qiling.\nBu sizga qiziq bo'masligi mumkin ammo botdagi xatoni aytsangiz bu bizga uni to'g'irlashga imkon beradi.Shu sababli iltimos bizga murojat qiling.</i>\n\nDasturchi va admin: @Nufada\nAdmin: @Cns_cewr"
    await message.answer(welcome_text)
