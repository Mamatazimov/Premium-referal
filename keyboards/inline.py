from aiogram.utils.keyboard import InlineKeyboardBuilder , InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from utils.channels import get_all_channel_id,get_all_channel_list


referral_blrd = InlineKeyboardBuilder()

referral_blrd.row(
    InlineKeyboardButton(text="Referrallarim ☑️", callback_data='my_referrals'),
    InlineKeyboardButton(text="Referrarim ☑️", callback_data='my_referrar'),
    )
referral_blrd.row(
    InlineKeyboardButton(text="Promo-code olish ☑️", callback_data='get_promo-code'),
    InlineKeyboardButton(text="Promo-code haqida ☑️", callback_data='promo-code_info'),
    )


referral_blrd_kb = referral_blrd.as_markup() #referral bo'limi keyboardi

to_back = InlineKeyboardBuilder()
to_back.row(InlineKeyboardButton(text="Orqaga 🔙", callback_data="to_back_ref"))
to_back_kb = to_back.as_markup() # orqaga harakatlanish uchun keyboard ref

user_profile = InlineKeyboardBuilder()
user_profile.row(
    InlineKeyboardButton(text="Mening ma'lumotlarim 📄",callback_data="user_info"),
    InlineKeyboardButton(text="Mening promo-codelarim 📄",callback_data="my_promocodes")
)
user_profile_kb = user_profile.as_markup() #foydalanuvchi bo'limi keyboardi

to_back_profile = InlineKeyboardBuilder()
to_back_profile.row(InlineKeyboardButton(text="Orqaga 🔙", callback_data="to_back_profile"))
to_back_profile_kb = to_back_profile.as_markup() # orqaga harakatlanish uchun keyboard profile


admin_menu = InlineKeyboardBuilder()
admin_menu.row(
    InlineKeyboardButton(text="Userni ma'lumotli",callback_data="user_info_admin_menu_button"),
    InlineKeyboardButton(text="Promo-codeni aktivsizlantirish",callback_data="promo-code_is_used_button")
)
admin_menu.row(
    InlineKeyboardButton(text="Statistika",callback_data="stat_admin_menu"),
    InlineKeyboardButton(text="Majburiy kanal obunasi",callback_data="mandatory_subscription"),
)
admin_menu.row(
    InlineKeyboardButton(text="Referrarga +5point",callback_data="add_point_rr"),
    InlineKeyboardButton(text="Barchaga xabar jo'natish",callback_data="send_to_all_users")
)
admin_menu_kb = admin_menu.as_markup()

channel_menu = InlineKeyboardBuilder()
channel_menu.row(
InlineKeyboardButton(text="Kanal qo'shish",callback_data="add_channel"),
InlineKeyboardButton(text="kanal o'chirish",callback_data="rem_channel")
)
channel_menu_kb = channel_menu.as_markup()

async def need_sub_channel_kb():
    need_sub_channel = InlineKeyboardBuilder()
    all_channel_len = len(get_all_channel_id())
    if all_channel_len != 0:
        all_channel = await get_all_channel_list()
        i = 0
        for info in all_channel:
            i += 1
            if info:  
                need_sub_channel.row(InlineKeyboardButton(text=f"Kanal {i}", url=f"https://t.me/{info[1:]}"))
    return need_sub_channel.as_markup()


prince_menu = InlineKeyboardBuilder()
prince_menu.row(
    InlineKeyboardButton(text="O'yinlar 🎮",callback_data="games"),
    InlineKeyboardButton(text="Dasturlar 📱",callback_data="programs")
)

prince_menu_kb = prince_menu.as_markup()


games_prince=InlineKeyboardBuilder()
games_prince.row(
    InlineKeyboardButton(text="Pubg",callback_data="pubg"),
    InlineKeyboardButton(text="Supercell o'yinlari",callback_data="supercell")
)
prince_menu.row(
    InlineKeyboardButton(text="Orqaga 🔙",callback_data="to_back_prince")
)
games_prince_kb=games_prince.as_markup()


programs_prince = InlineKeyboardBuilder()
programs_prince.row(
    InlineKeyboardButton(text="Telegram premium 👾",callback_data="tg_premium"),
    InlineKeyboardButton(text="Telegram stars ✨",callback_data="tg_star")
)
prince_menu.row(
    InlineKeyboardButton(text="Orqaga 🔙",callback_data="to_back_prince")
)
programs_prince_kb = programs_prince.as_markup()


supercell_games = InlineKeyboardBuilder()
supercell_games.row(
    InlineKeyboardButton(text="Clash of clans",callback_data="coc"),
    InlineKeyboardButton(text="Clash royale",callback_data="cr"),
    InlineKeyboardButton(text="Brawl stars ✨",callback_data="bs")
)
supercell_games.adjust(2)
supercell_games_kb = supercell_games.as_markup()


back_to_supercell_kb = InlineKeyboardBuilder().row(InlineKeyboardButton(text="Orqaga 🔙",callback_data="back_to_s")).as_markup()
