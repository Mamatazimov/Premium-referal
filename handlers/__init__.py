from aiogram import Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery

from handlers.start import start_command
from handlers.help import help_command
from handlers.messages import message_answers,registration,get_to_admin_user_id,inactive_promo,add_channel_msg,rem_channel_msg,add_point_refr_msg,send_message_all
from handlers.callback import Check_user_info,Inactive,Channels,Add_points_rr,Send_msg_all,tg_pr,tg_sr,clashroyal,brawlstars,clashofclans,sepercell_gm,pubg_uc,send_message_all_admin,to_back_ref_link, my_referrar,referrallarim,user_informations,user_promo,profile_menu,give_promo,promo_info,user_info_admin_menu,promo_code_is_used,users_stat,mandatory_channels,add_channel_cq,rem_channel_cq,add_point_refr,program_prince,games_prince
from keyboards.reply import reply_messages_list
from handlers.start import Registration




def register_handlers(dp: Dispatcher):
    dp.message(CommandStart())(start_command)
    dp.message(Command("help"))(help_command)
    dp.message(lambda message: message.text in reply_messages_list)(message_answers)
    dp.message(Registration.waiting_for_phone)(registration)
    dp.message(Check_user_info.waiting_for_user_id)(get_to_admin_user_id)
    dp.message(Inactive.waiting_for_promo)(inactive_promo)
    dp.message(Channels.waiting_for_channel_id1)(add_channel_msg)
    dp.message(Channels.waiting_for_channel_id2)(rem_channel_msg)
    dp.message(Add_points_rr.waiting_for_user_id)(add_point_refr_msg)
    dp.message(Send_msg_all.waiting_for_message)(send_message_all)
    dp.callback_query(lambda callback_query: callback_query.data == "tg_premium")(tg_pr)
    dp.callback_query(lambda callback_query: callback_query.data == "tg_star")(tg_sr)
    dp.callback_query(lambda callback_query: callback_query.data == "pubg")(pubg_uc)
    dp.callback_query(lambda callback_query: callback_query.data == "cr")(clashroyal)
    dp.callback_query(lambda callback_query: callback_query.data == "bs")(brawlstars)
    dp.callback_query(lambda callback_query: callback_query.data == "coc")(clashofclans)
    dp.callback_query(lambda callback_query: callback_query.data in ["supercell","back_to_s"])(sepercell_gm)
    dp.callback_query(lambda callback_query: callback_query.data == "games")(games_prince)
    dp.callback_query(lambda callback_query: callback_query.data == "programs")(program_prince)
    dp.callback_query(lambda callback_query: callback_query.data == "to_back_ref")(to_back_ref_link)
    dp.callback_query(lambda callback_query: callback_query.data == "my_referrals")(referrallarim)
    dp.callback_query(lambda callback_query: callback_query.data == "my_referrar")(my_referrar)
    dp.callback_query(lambda callback_query: callback_query.data == "to_back_ref")(my_referrar)
    dp.callback_query(lambda callback_query: callback_query.data == "to_back_profile")(profile_menu)
    dp.callback_query(lambda callback_query: callback_query.data == "user_info")(user_informations)
    dp.callback_query(lambda callback_query: callback_query.data == "my_promocodes")(user_promo)
    dp.callback_query(lambda callback_query: callback_query.data == "get_promo-code")(give_promo)
    dp.callback_query(lambda callback_query: callback_query.data == "promo-code_info")(promo_info)
    dp.callback_query(lambda callback_query: callback_query.data == "user_info_admin_menu_button")(user_info_admin_menu)
    dp.callback_query(lambda callback_query: callback_query.data == "promo-code_is_used_button")(promo_code_is_used)
    dp.callback_query(lambda callback_query: callback_query.data == "stat_admin_menu")(users_stat)
    dp.callback_query(lambda callback_query: callback_query.data == "mandatory_subscription")(mandatory_channels)
    dp.callback_query(lambda callback_query: callback_query.data == "add_channel")(add_channel_cq)
    dp.callback_query(lambda callback_query: callback_query.data == "rem_channel")(rem_channel_cq)
    dp.callback_query(lambda callback_query: callback_query.data == "add_point_rr")(add_point_refr)
    dp.callback_query(lambda callback_query: callback_query.data == "send_to_all_users")(send_message_all_admin)








    











