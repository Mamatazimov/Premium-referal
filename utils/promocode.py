import random
import string
import sqlite3

from utils.referral_link import get_user_points

# promo code generatsiya qilish
def generate_promo_code():
    promo = "".join(random.choices(string.ascii_uppercase + string.digits,k=8))
    return promo

#promo code yaratish
def create_promo_code(user_id,required_points):
    conn = sqlite3.connect("referral.db")
    cursor = conn.cursor()

    result = get_user_points(user_id=user_id)

    if result != 0 and result >= required_points:
        promo_code = generate_promo_code()

        cursor.execute("""
                UPDATE users SET points = points - ?
                       WHERE user_id = ?
                """,(required_points,user_id,))
        
        cursor.execute("INSERT INTO promocodes(code,user_id) VALUES (?,?)",(promo_code,user_id))

        conn.commit()
        conn.close()
        return promo_code
    else:
        conn.close()
        return result

#promo codeni tekshirish
def get_promo_code(user_id):
    conn = sqlite3.connect("referral.db")
    cursor = conn.cursor()

    cursor.execute("SELECT code,is_used FROM promocodes WHERE user_id = ?",(user_id,))
    result = cursor.fetchall()
    conn.close()
    return result if result else 0

# barcha promo codeni listga yuklab olish
def all_promo_code():
    conn = sqlite3.connect("referral.db")
    cursor = conn.cursor()

    cursor.execute("SELECT code FROM promocodes")
    result = cursor.fetchall()
    result_list = []
    for r in result:
        result_list.append(r[0])
    
    conn.close()
    return result_list

# promo codeni aktivsizlantirish
def inactive_promo(promo_code):
    conn = sqlite3.connect("referral.db")
    cursor = conn.cursor()
    if promo_code in all_promo_code():
  
        cursor.execute("UPDATE promocodes SET is_used = 1 WHERE code = ?",(promo_code,))
        conn.commit()
        conn.close()
        return 1
    else:
        conn.close()
        return 0
    
# promo code statistikasi
def aktive_promo_stat():
    conn = sqlite3.connect("referral.db")
    cursor = conn.cursor()
  
    cursor.execute("SELECT is_used from promocodes WHERE is_used = ?",(0,))
    active = len(cursor.fetchall())

    conn.close()
    return active

def inaktive_promo_stat():
    conn = sqlite3.connect("referral.db")
    cursor = conn.cursor()
  
    cursor.execute("SELECT is_used from promocodes WHERE is_used = ?",(1,))
    active = len(cursor.fetchall())

    conn.close()
    return active
