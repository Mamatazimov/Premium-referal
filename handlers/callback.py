from aiogram import types
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage


from keyboards.inline import  to_back_kb , referral_blrd_kb,user_profile_kb,to_back_profile_kb,channel_menu_kb,games_prince_kb,programs_prince_kb,supercell_games_kb,back_to_supercell_kb
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

# O'yinlar bo'limi
async def games_prince(cq: types.CallbackQuery):
    await cq.message.edit_text("O'yinlar bo'limi 🎮",reply_markup=games_prince_kb)

# Ilovalar bo'limi
async def program_prince(cq: types.CallbackQuery):
    await cq.message.edit_text("Ilovalar bo'limi 📱", reply_markup=programs_prince_kb)

# Pubg uc narxlari
async def pubg_uc(cq: types.CallbackQuery):
    await cq.message.edit_text(f"<b>Pubg mobile o'yinidagi uc narxlari 👇:</b>\n\n"
                               "<i>60 uc - 12k so'm</i>\n"
                               "<i>325 uc - 58k so'm</i>\n"
                               "<i>660 uc - 115k so'm</i>\n"
                                "<i>1800 uc - 285k so'm</i>\n"
                                "<i>3850 uc - 560k so'm</i>\n"
                                "<i>8100 uc - 1120k so'm</i>\n\n"
                                "<b>Adminlar: <i>@Nufada , @Cns_cewr</i></b>"
                               )
    
# Supercell narxlari
async def sepercell_gm(cq: types.CallbackQuery):
    await cq.message.edit_text(f"Supercell o'yinni tanlang",reply_markup=supercell_games_kb)

# Clash of clans
async def clashofclans(cq: types.CallbackQuery):
    await cq.message.edit_text("<b>Clash of clans o'yinidagi gem narxlari 👇:</b>\n\n"
                               "<i>80 gem - 14k so'm</i>\n"
                               "<i>500 gem - 69k so'm</i>\n"
                               "<i>1200 gem - 129k so'm</i>\n"
                               "<i>2500 gem - 249k so'm</i>\n"
                                "<i>6500 gem - 640k so'm</i>\n"
                                "<i>14000 gem - 1200k so'm</i>\n"
                                "<i>Gold pass - 90k so'm</i>\n\n"
                                "<i>Agarda personajlarga yoki bazaga skinlar kerak bo'lsa adminlarga murojat qilib narxlarni kelishishingiz mumkin.</i>\n"
                                "<b>Adminlar: <i>@Nufada , @Cns_cewr</i></b>",reply_markup=back_to_supercell_kb
                               )

# Clash royal
async def clashroyal(cq: types.CallbackQuery):
    await cq.message.edit_text("<b>Clash royal o'yinidagi gem narxlari 👇:</b>\n\n"
                               "<i>80 gem - 14k so'm</i>\n"
                               "<i>500 gem - 69k so'm</i>\n"
                               "<i>1200 gem - 129k so'm</i>\n"
                               "<i>2500 gem - 249k so'm</i>\n"
                                "<i>6500 gem - 640k so'm</i>\n"
                                "<i>14000 gem - 1200k so'm</i>\n"
                                "<i>Almaz pass - 145k so'm</i>\n\n"
                                "<i>Agarda personajlarga yoki bazaga skinlar kerak bo'lsa adminlarga murojat qilib narxlarni kelishishingiz mumkin.</i>\n"
                                "<b>Adminlar: <i>@Nufada , @Cns_cewr</i></b>",reply_markup=back_to_supercell_kb
                               )

# Squad busters 
async def brawlstars(cq: types.CallbackQuery):
    await cq.message.edit_text("<b>Brawl stars o'yinidagi  narxlari 👇:</b>\n\n"
                               "<i>80 gem - 14k so'm</i>\n"
                               "<i>500 gem - 69k so'm</i>\n"
                               "<i>1200 gem - 129k so'm</i>\n"
                               "<i>2500 gem - 249k so'm</i>\n"
                                "<i>6500 gem - 640k so'm</i>\n"
                                "<i>14000 gem - 1200k so'm</i>\n"
                                "<i>Gold pass - 90k so'm</i>\n\n"
                                "<i>Agarda personajlarga yoki bazaga skinlar kerak bo'lsa adminlarga murojat qilib narxlarni kelishishingiz mumkin.</i>\n"
                                "<b>Adminlar: <i>@Nufada , @Cns_cewr</i></b>",reply_markup=back_to_supercell_kb)


# Telegram premium
async def tg_pr(cq: types.CallbackQuery):
    await cq.message.edit_text(
        "<b>Premium narxlari bilan tanishishingiz mumkin:</b>\n"
        "<b>Telegram akkauntizga kirib olib beriladi:</b>\n\n"
        "<i>1 oylik telegram premium: 52000 Uzs</i>\n"
        "<i>12 oylik telegram premium: 299000 Uzs</i>\n\n"
        "<b>Telegram akkauntizga kirmasdan olib beriladi:</b>\n\n"
        "<i>3 oylik telegram premium: 189000 Uzs</i>\n"
        "<i>6 oylik telegram premium: 239000 Uzs</i>\n"
        "<i>12 oylik telegram premium: 399000 Uzs</i>\n\n"
        "<i>Narxlar ma'qul kelgan bo'lsa adminlar:</i>\n"
        "<i>Admin 1  @Nufada</i>\n"
        "<i>Admin 2  @Cns_cewr</i>\n"
    )

# Telegram star
async def tg_sr(cq: types.CallbackQuery):
    await cq.message.edit_text("<b>Telegram stars narxlari bilan tanishishingiz mumkin:</b>\n\n"
                                "<i>100ta star - 27k so'm</i>\n"
                                "<i>150ta star - 40k so'm</i>\n"
                                "<i>250ta star - 65k so'm</i>\n"
                                "<i>350ta star - 85k so'm</i>\n"
                                "<i>500ta star - 120k so'm</i>\n"
                                "<i>750ta star - 180k so'm</i>\n"
                                "<i>1000ta star - 240k so'm</i>\n\n"
                                "<b>Adminlar: <i>@Nufada , @Cns_cewr</i></b>"
                               )







