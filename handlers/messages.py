import re
from aiogram.exceptions import TelegramBadRequest
from aiogram import types
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage


from keyboards.reply import main_keyboard
from config import Admin_Id
from keyboards.inline import referral_blrd_kb,user_profile_kb,admin_menu_kb
from utils import referral_link,promocode,channels



# asosiy menyu buttonlariga javob
async def message_answers(message: types.Message):



    if message.text == "Premium narxlari 💸" :
        message_answer = """
<b>Premium narxlari bilan tanishishingiz mumkin:</b>\n
<b>Telegram akkauntizga kirib olib beriladi:</b>\n
<b>1 oylik telegram premium:</b><i> 52000 Uzs</i>\n
<b>12 oylik telegram premium:</b><i> 299000 Uzs</i>\n
\n
<b>Telegram akkauntizga kirmasdan olib beriladi:</b>\n
<b>3 oylik telegram premium:</b><i> 189000 Uzs</i>\n
<b>6 oylik telegram premium:</b><i> 239000 Uzs</i>\n
<b>12 oylik telegram premium:</b><i> 399000 Uzs</i>\n
\n
<b>Narxlar ma'qul kelgan bo'lsa adminlar:</b>\n
<b>Admin 1 </b> @Nufada\n
<b>Admin 2 </b> @Cns_cewr\n
"""
        await message.answer(text=message_answer,parse_mode="HTML")

    
    elif message.text == "Referral tizimi 🫱🏼‍🫲🏽":
        user_id = message.from_user.id
        await message.answer(text=f"<b>Sizning referral link :</b>\n <code>https://t.me/Premium_duo_robot?start={user_id}</code>", reply_markup=referral_blrd_kb)


    elif message.text == "Adminlar 👥" :
        if message.from_user.id in Admin_Id:
            await message.answer("<b>Admin bo'limida man bilan mani beatifulll bro imga kirishga ruhsat berilgan.</b><i>Agar yana adminlar qo'shilgan bo'lsa quyidagi bo'limlardan biriga kirishiz mumkin:</i>",reply_markup=admin_menu_kb)
        else:
            await message.answer(f"<b>Bizning adminlar</b>:\n<b>Azimov:</b> @Nufada\nᅠᅠᅠᅠᅠᅠᅠᅠᅠᅠ: @Cns_cewr")
    
    elif message.text == "Profil 👤" :
        await message.answer(f"<b>Profil bo'limiga hush kelibsiz.\nPastdagi tugmalardan kerakligini tanlashiz mumkin</b>",reply_markup=user_profile_kb)

# ro'yhatdan o'tkazish
async def registration(message: types.Message,state: FSMContext):
    from main import bot
    UZ_PHONE_REGEX = r"^998\d{9}$"
    if message.contact is not None:
        user_id = message.from_user.id
        try:
            referrer_id = referral_link.get_user_referrer(user_id)[0]
        except:
            referrer_id = None
        phone_number = message.contact.phone_number
        if referrer_id == None:
            if referral_link.check_is_sub(user_id):
                referral_link.referrar_id_activating(user_id)
                referral_link.add_points(referrer_id, 0)
            await message.answer(f"Siz muvaffaqiyatli ro'yhatdan o'tdingiz",reply_markup=main_keyboard())
            await state.clear()
        elif referrer_id==user_id:
            if referral_link.check_is_sub(user_id):
                referral_link.referrar_id_activating(user_id)
            if referral_link.check_all(user_id):
                referral_link.add_points(referrer_id, 0)
            await message.answer(f"O'zingizni taklif qilishingiz mumkin emas",reply_markup=main_keyboard())
            await state.clear()
        else:
            if re.match(UZ_PHONE_REGEX,phone_number):
                if referral_link.check_is_sub(user_id):
                    referral_link.referrar_id_activating(user_id)
                    referral_link.add_points(referrer_id, 1)
                user = await bot.get_chat(referrer_id)
                rr_user = f"@{user.username}" or referrer_id
                await message.answer(f"Siz muvaffaqiyatli ro'yhatdan o'tdingiz va sizni chaqirgan inson: {rr_user}",reply_markup=main_keyboard())
                await state.clear()
            else:
                if referral_link.check_is_sub(user_id):
                    referral_link.referrar_id_activating(user_id)
                    referral_link.add_points(referrer_id,0)

                user = await bot.get_chat(referrer_id)
                rr_user = f"@{user.username}" or referrer_id
                await message.answer(f"Sizning telefon raqamingiz Uzbekistan davlatiga tegishli emasligi uchun biz sizni referraringizga sizni taklif qilgani uchun point bermaymiz.Buning sababi botda qoida buzarlik yo'llar bilan odam ko'paytirib tashlashni oldini olish uchun.\nSizning referraringiz: {rr_user}",reply_markup=main_keyboard())
                await state.clear()
    else:
        await message.answer(f"Telefon raqamni qabul qilishda muammo yuz berdi")
        await state.clear()

# adminga userni ma'lumotlarini berish
async def get_to_admin_user_id(message: types.Message,state: FSMContext):
    from main import bot

    user_id = message.text

    try:
        user_info = referral_link.get_user_info(user_id=user_id)
        my_ref = len(referral_link.get_user_referrals(user_id=user_id))

        user = await bot.get_chat(user_id)
        no_info = "Mavjud emas"
        firstN = user.first_name or no_info
        lastN = user.last_name or no_info
        userN = user.username or no_info

        if userN == no_info:
            userN = "Mavjud emas"
        else:
            userN = f"@{userN}"
        
        
        await message.answer(f"Ism: {firstN}\nFamiliya: {lastN}\nUsername: {userN}\nReferrallar soni: {my_ref}\nPointlar: {user_info[3]}\nUser id:{user_id}")
        await state.clear()

    except TelegramBadRequest:
        await message.answer(f"Telegram bad request hatosini jo'natdi")
        await state.clear()

    except Exception as xato:
        await message.answer(f"Nomalum hato: {xato}")

# admin promo-codeni aktivsizlantirishi
async def inactive_promo(message: types.Message,state: FSMContext):
    promo_code = message.text
    if promocode.inactive_promo(promo_code=promo_code) and promocode.inactive_promo(promo_code=promo_code) !=0:
        await message.answer(f"Promo-code muvaffaqiyatli aktivsizlantirildi {promocode.inactive_promo(promo_code=promo_code)}")
    elif promocode.inactive_promo(promo_code=promo_code) == 0:
        await message.answer("Promo-code ma'lumotlar bazasida topilmadi")
    else:
        await message.answer("Promo-code aktivsizlantirishda xatolik yuz berdi")
    await state.clear()

# admin kanal qo'shishi
async def add_channel_msg(message: types.Message,state: FSMContext):
    channel_id = message.text
    result = channels.add_channel(channel_id=channel_id)

    if result == 1:

        if result != 0:
            await message.answer("Kanal idsi bazaga muvaffaqiyatli joylandi:")
            await state.clear()

    elif result == "Xato":
        await message.answer("ID raqamdan iborat bo'lsin")
        await state.clear()
    else:
        await message.answer(f"Botga faqat 5ta gacha kanal idsi joylash mumkin :")
        await state.clear()

# admin kanal o'chirishi
async def rem_channel_msg(message: types.Message,state: FSMContext):
    numofchan = len(channels.get_all_channel_id())
    channel_id = message.text 
    if numofchan > 0:
        channels.delete_channel(channel_id=channel_id)
        await message.answer("Kanal idsi bazadan muvaffaqiyatli o'chirildi:")
    else:
        await message.answer(f"O'chiradigan kanal idsi yo'q :")
    await state.clear()

# referrarga 5point qo'shuv xabari
async def add_point_refr_msg(message: types.Message,state:FSMContext):
    user_id = message.text
    try:
        referrar_id = referral_link.get_user_referrer(user_id)[0]
        if referrar_id == None:
            await message.answer("Foydalanuvchi referrari topilmadi")
        else:
            if user_id == referrar_id:
                await message.answer("User o'zini o'zi referrar qilgani uchun point qo'shilmadi")
            else:
                referral_link.add_points(referrar_id,5)
                await message.answer("Userning referrariga muaffaqiyatli 5point qo'shildi")

    except IndexError:
        await message.answer("Foydalanuvchi referrari topilmadi")

    
    
#caption