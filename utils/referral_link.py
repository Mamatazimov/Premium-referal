import sqlite3


def add_user(user_id,referrer_id=None):
    conn = sqlite3.connect("referral.db")
    cursor = conn.cursor()

    cursor.execute("""
            INSERT OR IGNORE INTO users(user_id, referrer_id)
                   VALUES (?, ?)
        """,(user_id, referrer_id))
    
    conn.commit()
    conn.close()

def all_referrer_id():
    conn = sqlite3.connect("referral.db")
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM users WHERE referrer_id IS NULL")
    result = cursor.fetchall()
    result_list = []
    for r in result:
        result_list.append(r[0])
    
    conn.close()
    return result_list

def add_active_referrar(user_id):
    conn = sqlite3.connect("referral.db")
    cursor = conn.cursor()
    if user_id in all_referrer_id():
        cursor.execute("UPDATE users SET active_referrer_id = 1 WHERE user_id = ?",(user_id,))
        conn.commit()
        conn.close()
        return 1
    else:
        conn.close()
        return 0

def get_user_points(user_id):
    conn = sqlite3.connect("referral.db")
    cursor = conn.cursor()

    cursor.execute("SELECT points FROM users WHERE user_id = ?",(user_id,))
    result = cursor.fetchone()

    conn.close()

    return result[0] if result else 0

def add_points(user_id, points):
    conn = sqlite3.connect("referral.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users SET points = points + ?
                   WHERE user_id = ?
        """,(points,user_id))
    
    conn.commit()
    conn.close()

def referrar_id_activating(user_id):
    conn = sqlite3.connect("referral.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET active_referrer_id = 1 WHERE user_id = ?",(user_id,))
    conn.commit()
    conn.close()

def check_active_referrer_id(user_id):

    conn = sqlite3.connect("referral.db")
    cursor = conn.cursor()

    cursor.execute("SELECT active_referrer_id FROM users WHERE user_id = ?",(user_id,))
    result = cursor.fetchone()

    conn.close()
    return result[0] if result else 0

def check_user(user_id):
    conn = sqlite3.connect("referral.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT EXISTS(SELECT 1 FROM users WHERE user_id = ?)
        """,(user_id,))
    result = cursor.fetchone()[0]
    
    conn.close()
    if result == 1:
        return True
    elif result == 0:
        return False

def get_user_referrals(user_id):
    conn = sqlite3.connect("referral.db")
    cursor = conn.cursor()

    cursor.execute("SELECT referrer_id FROM users WHERE referrer_id = ?",(user_id,))
    result = cursor.fetchall()

    conn.close()
    return result

def get_user_referrer(user_id):
    conn = sqlite3.connect("referral.db")
    cursor = conn.cursor()

    cursor.execute("SELECT referrer_id FROM users WHERE user_id = ?",(user_id,))
    result = cursor.fetchone()

    conn.close()
    return result

def get_user_info(user_id):
    conn = sqlite3.connect("referral.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE user_id = ?",(user_id,))
    result = cursor.fetchone()

    conn.close()
    return result

def get_users_stat():
    conn = sqlite3.connect("referral.db")
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM users")
    result = len(cursor.fetchall())

    conn.close()
    return result

def get_referral_users_stat():

    conn = sqlite3.connect("referral.db")
    cursor = conn.cursor()

    cursor.execute("SELECT referrer_id FROM users WHERE referrer_id IS NULL")
    result = len(cursor.fetchall())

    conn.close()
    return result

def add_points_active(user_id,point):
    conn = sqlite3.connect("referral.db")
    cursor = conn.cursor()
    if check_active_referrer_id(user_id):
        cursor.execute("UPDATE users SET points = points + ? WHERE user_id = ?",(point,user_id))
        conn.commit()
        conn.close()
        return 1
    else:
        return 0
    
def check_is_sub(user_id):
    conn = sqlite3.connect("referral.db")
    cursor = conn.cursor()

    cursor.execute("SELECT is_sub FROM users WHERE user_id = ?",(user_id,))
    result = cursor.fetchone()

    conn.close()
    return result[0] if result else 0

def activate_is_sub(user_id):

    conn = sqlite3.connect("referral.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET is_sub = 1 WHERE user_id = ?",(user_id,))
    conn.commit()
    conn.close()

def check_all(user_id):
    is_sub = check_is_sub(user_id)
    check_activ = check_active_referrer_id(user_id)
    if is_sub and check_activ:
        return 1
    else:
        return 0

def get_all_user():
    conn = sqlite3.connect("referral.db")
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM users")
    result = cursor.fetchall()
    conn.close()
    return result if result else None