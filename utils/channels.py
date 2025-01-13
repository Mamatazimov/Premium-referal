import sqlite3



def get_all_channel_id():
    try:
        conn = sqlite3.connect("referral.db")
        cursor = conn.cursor()

        cursor.execute("SELECT channel_id FROM channels")
        result = cursor.fetchall()
        result_list = []
        if result:
            for r in result:
                result_list.append(r[0])
        conn.close()
        return result_list
    except sqlite3.OperationalError:
        conn.close()
        return []


def add_channel(channel_id):
    conn = sqlite3.connect("referral.db")
    cursor = conn.cursor()
    result = len(get_all_channel_id())
    try:
        if result <= 4:

            channel_id=int(channel_id)
            cursor.execute("""
                    INSERT OR IGNORE INTO channels(channel_id)
                        VALUES (?)
                """,(channel_id,))
                    
            conn.commit()
            conn.close()
            return 1
        else:
            channel_id=int(channel_id)
            return 0
    except Exception:
        conn.close()
        return "Xato"



def delete_channel(channel_id):
    conn = sqlite3.connect("referral.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM channels WHERE channel_id = ?",(channel_id,))
    
    conn.commit()
    conn.close

async def get_all_channel_list():
    from main import bot
    channels_id = get_all_channel_id()
    list_for_channel = []
    for channel_id in channels_id:
        channel_id = int(f"-100{channel_id}")
        chat = await bot.get_chat(channel_id)
        if chat.username:
            channel_url = f"@{chat.username}"
            list_for_channel.append(channel_url)
        else:
            list_for_channel.append(None)
    return list_for_channel

async def check_user_in_channel(channel_username: str, user_id: int):
    from main import bot
    try:
        chat_member = await bot.get_chat_member(chat_id=channel_username, user_id=user_id)
        if chat_member.status in ["member", "administrator", "creator"]:
            return True  
        return False  
    except Exception as e:
        print(f"Xato: {e}")
        return False

        
