from aiogram import types
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage


from keyboards.inline import  to_back_kb , referral_blrd_kb,user_profile_kb,to_back_profile_kb,channel_menu_kb
from utils.referral_link import get_user_referrals, get_user_referrer,get_user_points,get_user_info,get_users_stat,get_referral_users_stat
from utils.promocode import get_promo_code,create_promo_code,aktive_promo_stat,inaktive_promo_stat
from utils.channels import add_channel,delete_channel,get_all_channel_id


class Check_user_info(StatesGroup):
    waiting_for_user_id = State()  

class Inactive(StatesGroup):
    waiting_for_promo = State()  

class Channels(StatesGroup):
    waiting_for_channel_id1 = State()  
    waiting_for_channel_id2 = State()  

class Add_points_rr(StatesGroup):
    waiting_for_user_id = State()

class Send_msg_all(StatesGroup):
    waiting_for_message = State()

# foydalanuvchining referral pointlari va referallari bo'limi uchun funksiya
async def referrallarim(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_points = get_user_points(user_id=user_id) or 0
    my_ref = len(get_user_referrals(user_id=user_id))
    await callback_query.message.edit_text(f"<b>Sizning referrallaringiz soni: <i>{my_ref}</i> \nSizning pointlaringiz</b>: <i>{user_points}</i>", reply_markup=to_back_kb)

# ortga qaytarish uchunfunksiya
async def to_back_ref_link(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await callback_query.message.edit_text(text=f"<b>Sizning referral link :</b>\n <code>https://t.me/Premium_duo_robot?start={user_id}</code>", reply_markup=referral_blrd_kb)

# foydalanuvchining referrari bo'limi uchun funksiya
async def my_referrar(callback_query: types.CallbackQuery):
    from main import bot

    user_id = callback_query.from_user.id
    if get_user_referrer(user_id)[0]:
        

        referrar_user = get_user_referrer(user_id)[0]
        user = await bot.get_chat(referrar_user)


        firstN = user.first_name 
        lastN = user.last_name or "Mavjud emas"
        if user.username:
            userN = f"@{user.username}"
        else:
            userN = "Mavjud emas"



        await callback_query.message.edit_text(text=f"Sizning chaqiruvchingiz:\nIsmi: {firstN}\nFamiliyasi: {lastN}\nUsername: {userN}",reply_markup=to_back_kb)

    else:
        await callback_query.message.edit_text(text=f"Siz o'zingiz qo'shilgansiz , sizda hech qanday referrar yo'q.",reply_markup=to_back_kb)

# foydalanuvchu ma'lumotlari bo'limi funksiyasi
async def user_informations(callback_query: types.CallbackQuery):
    from main import bot
    try:
        user_id = callback_query.from_user.id
        user_info = get_user_info(user_id=user_id)
        my_ref = len(get_user_referrals(user_id=user_id))


        user = await bot.get_chat(user_id)
        no_info = "Mavjud emas"
        firstN = user.first_name or no_info
        lastN = user.last_name or no_info
        userN = f"@{user.username}" or no_info

        try:
            await callback_query.message.edit_text(f"Ismingiz: {firstN}\nFamiliyangiz: {lastN}\nUsername: {userN}\nSizning referrallaringiz soni: {my_ref}\nSizning pointlaringiz: {user_info[3]}",reply_markup=to_back_profile_kb)
        except TelegramBadRequest:
            await callback_query.message.edit_text(f"Iltimos tugmalarni bosib tashlamang!!!\nAgar bosib tashlasangiz pointlaringizni 0 qilib qo'yaman :)")
    except TypeError:
        await callback_query.message.edit_text(f"Uzur ma'lumotlar bazasida qandaydir hatolik paydo bo'ldi.\n/start kamandasini bosib registratsiyadan o'tib qo'yishingizni so'rayman")

# Userni promo-codelari
async def user_promo(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    promo_code = get_promo_code(user_id)
    try:
        if promo_code[0]:
            promo_txt = ""

            for promo in promo_code:
                promo = list(promo)
                if promo[1] == 1:
                    continue
                promo_txt += f"<code>{str(promo[0])}</code> "
            if promo_txt == "":
                await callback_query.message.edit_text(f"<i>Sizda hech qanday promo-code yo'q</i>",reply_markup=to_back_profile_kb)
            else:
                await callback_query.message.edit_text(f"<b>Sizning aktiv promo-codelaringiz:</b>\n{promo_txt}",reply_markup=to_back_profile_kb)
        else:
            await callback_query.message.edit_text(f"<i>Sizda hech qanday promo-code yo'q</i>",reply_markup=to_back_profile_kb)
    except:
        await callback_query.message.edit_text(f"<i>Sizda hech qanday promo-code yo'q</i>",reply_markup=to_back_profile_kb)

# menu
async def profile_menu(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(f"Profil bo'limiga hush kelibsiz.\nPastdagi tugmalardan kerakligini tanlashiz mumkin",reply_markup=user_profile_kb)

# userga promo-code berish
async def give_promo(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    promo = create_promo_code(user_id=user_id,required_points=100)
    if promo:
        await callback_query.message.answer(f"<code>{promo}</code>")
    else:
        await callback_query.message.edit_text(f"Sizning pointingiz promo-codega yetmaydi!")

# promo-codelar haqida malumot beruvchi funksiya
async def promo_info(cq: types.CallbackQuery):
    promo_info_txt = "<b>Sizga promo-codelar haqida ma'lumot bermoqchiman.</b>\n\n<i>Siz botga o'z referrallaringizni chaqirib har bir referral uchun 1 pointdan, agar referrallaringiz bizdan premium sotib olishsa ularning har biridan 5 pointdan  olishingiz mumkin.\n\nSiz pointlaringizni 100 taga yetganda promo-codega aylantirib olishingiz mumkin, va adminlardan biriga tashlab bersangiz ular sizga 1oylik telegram premiumni tekinga olib berishadi.</i>"
    await cq.message.edit_text(promo_info_txt)

# admin user_idni jo'natishi uchun so'rov
async def user_info_admin_menu(cq: types.CallbackQuery,state: FSMContext):
    await cq.message.answer("Foydalanuvchining id sini tashlang:")
    await state.set_state(Check_user_info.waiting_for_user_id)

# promo-codeni aktivsizlantirish
async def promo_code_is_used(cq: types.CallbackQuery,state: FSMContext):
    await cq.message.answer("Foydalanuvchining promo_codeni tashlang:")
    await state.set_state(Inactive.waiting_for_promo)

# bot statistikasi
async def users_stat(cq: types.CallbackQuery):
    all_user = get_users_stat()
    activ_promo = aktive_promo_stat()
    inactive_promo = inaktive_promo_stat()
    without_ref_users_stat = get_referral_users_stat()
    with_ref_users_stat = int(all_user) - int(without_ref_users_stat)
    await cq.message.answer(f"Barcha foydalanuvchilar soni: {all_user}\nFaol promo-codelar soni: {activ_promo}\nNofaol promo-codelar soni: {inactive_promo}\nBarcha promo-codelar soni: {activ_promo+inactive_promo}\nO'zi qo'shilgan foydalanuvchilar soni: {without_ref_users_stat}\nReferraldan qo'shilgan foydalanuvchilar soni: {with_ref_users_stat}")

# admin majburiy kanallarni qo'shib , olib tashlashi uchun menu funksiya
async def mandatory_channels(cq: types.CallbackQuery):
    all_channel = get_all_channel_id()
    all_channel_len = len(all_channel)
    if all_channel_len == 0:
        await cq.message.answer("Ro'yhat bo'm-bo'sh",reply_markup=channel_menu_kb)
    else:
        text=""
        for id in all_channel:
            text+=f"<code> {id} </code>"
        await cq.message.answer(f"Malumotlar bazasidaki kanallar idsi:{text}",reply_markup=channel_menu_kb)

# kanal qo'shish uchun habar
async def add_channel_cq(cq: types.CallbackQuery,state:FSMContext):
    await cq.message.answer("Qo'shmoqchi bo'lgan kanalingni id sini tashla.\nQaysi adminsan bilmeman lekin tugmala bilan o'ynama.")
    await state.set_state(Channels.waiting_for_channel_id1)

# kanal o'chirish uchun habar
async def rem_channel_cq(cq: types.CallbackQuery,state:FSMContext):
    await cq.message.answer("O'chirmoqchi bo'lgan kanalingni id sini tashlang.\nQaysi adminsan bilmeman lekin tugmala bilan o'ynama.")
    await state.set_state(Channels.waiting_for_channel_id2)

# referrarga point qo'shish
async def add_point_refr(cq: types.CallbackQuery,state:FSMContext):
    await cq.message.answer("Foydalanuvchi id sini tashlang:")
    await state.set_state(Add_points_rr.waiting_for_user_id)

# Barchaga habar jo'natish 1-boshqish
async def send_message_all_admin(cq: types.CallbackQuery,state:FSMContext):
    await cq.message.answer("Xabar matnini tashlang")
    await state.set_state(Send_msg_all.waiting_for_message)


