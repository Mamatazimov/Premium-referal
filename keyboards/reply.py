from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Profil 👤 " ), KeyboardButton(text="Premium narxlari $")],
            [KeyboardButton(text="Adminlar 👥"),KeyboardButton(text="Referral tizimi ⋔")]
        ],
        resize_keyboard=True
    )

    return keyboard

reply_messages_list = [
    "Profil 👤","Premium narxlari $","Adminlar 👥","Referral tizimi ⋔"
]

def phone_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
        keyboard=[[KeyboardButton(text="Telefon raqamingizni tekshirish 📞",request_contact=True)]]
    )
    return keyboard
