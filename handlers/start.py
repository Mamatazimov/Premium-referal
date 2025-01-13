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
    
# userning referral liknini bazaga saqlab olish
    if args:
        try:
            referrer_id = int(args[0])
            referral_link.add_user(user_id,referrer_id)

        except ValueError:
            await message.answer("Referal havola noto'g'ri.")
            return
    else:
        referral_link.add_user(user_id)
# userni kanallarga obuna bo'lganini tekshirish
    for channel in channels:
        if channel and not await check_user_in_channel(channel,user_id):
            all_subscribed = False
            break
    if all_subscribed:
        referral_link.activate_is_sub(user_id) # user barcha kanallarga obuna bo'lgan bo'lsa uni activ referrar qilib bazaga belgilash
            # user activ_userga aylanishi uchun uni nomerini tekshirish
        if referral_link.check_active_referrer_id(user_id):
            await message.answer("Hush kelibsiz!",reply_markup=main_keyboard())
        else:
            await message.answer("Iltimos telefon raqamingizni kiriting!",reply_markup=phone_keyboard())
            await state.set_state(Registration.waiting_for_phone)
        

    else:
        keyboard = await need_sub_channel_kb()
        await message.answer("<b>Siz bizning kanallarimizga a'zo bo'lmadingiz.</b>\n<i>Iltimos a'zo bo'lib qayta /start kamandasini bosing</i>",reply_markup=keyboard)




