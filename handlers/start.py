import re
from aiogram import types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from utils import referral_link
from keyboards.reply import main_keyboard, phone_keyboard
from utils.channels import get_all_channel_list, check_user_in_channel
from keyboards.inline import need_sub_channel_kb


class Registration(StatesGroup):
    waiting_for_phone = State()



async def start_command(message: types.Message,state: FSMContext):

    args = message.text.split()[1:]
    user_id = message.from_user.id
    channels = await get_all_channel_list()
    all_subscribed = True
    

    

    if args:
        try:
            referrer_id = int(args[0])

        except ValueError:
            await message.answer("Referal havola noto'g'ri.")
            return

        if referral_link.check_user(user_id=user_id) is True:
            await message.answer("Siz allaqachon ro'yhatdan o'tgansiz")
        else:
            if referrer_id == user_id:
                if referral_link.check_user(user_id=referrer_id) is False:
                    await message.answer("Siz o'zingizn referral qilmoqchilingiz uchun hatolik yuz berdi.\nIltimos /start kamandasini bosib o'zingizni ro'yhatdan o'tkazing.")
                else:
                    await message.answer("Siz o'zingizni referal qilmoqchi bo'ldingiz ammo siz allaqachon ro'yhatdan o'tgansiz",reply_markup=main_keyboard())

            elif referral_link.check_user(user_id=referrer_id) is False:
                referral_link.add_user(user_id,referrer_id)
                await message.answer("Sizning referraringiz ya'ni chaqiruvchingiz haqidagi ma'lumot bizning bazada topilmadi.\nBu degani siz noto'g'ri link bilan ro'yhatdan o'tdingiz.",reply_markup=main_keyboard())
            else:
                await message.answer("Tekshiruv uchun iltimos telefon raqamingizni jo'nating",reply_markup=phone_keyboard())
                await state.set_state(Registration.waiting_for_phone)
                await state.update_data(name=args)

    else:
        if referral_link.check_user(user_id=user_id) is True:
            await message.answer("Hush kelibsiz",reply_markup=main_keyboard())
        else:
            await message.answer("Tekshiruv uchun iltimos telefon raqamingizni jo'nating",reply_markup=phone_keyboard())
            await state.set_state(Registration.waiting_for_phone)
            await state.update_data(name=args)
  
"""
    for channel in channels:
        if channel and not await check_user_in_channel(channel,user_id):
            all_subscribed = False
            break
    if all_subscribed:
        pass
    else:
        keyboard = await need_sub_channel_kb()
        await message.answer("Siz bizning kanallarimizga a'zo bo'lmadingiz. Iltimos a'zo bo'lib qayta /start kamandasini bosing",reply_markup=keyboard)
        return
"""



