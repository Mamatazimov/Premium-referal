import sqlite3

def init_db():
    conn = sqlite3.connect("referral.db")
    cursor = conn.cursor()

    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS users(
                   id INTEGER PRIMARY KEY,
                   user_id INTEGER UNIQUE,
                   referrer_id INTEGER,
                   active_referrer_id BOOLIEAN DEFAULT 0,
                   points INTEGER DEFAULT 0                   
                   )
        """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS promocodes(
                    id INTEGER PRIMARY KEY,
                    code TEXT UNIQUE NOT NULL,
                    user_id INTEGER NOT NULL,
                    is_used BOOLIEAN DEFAULT 0,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)  
                   )
        """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS channels(
                   id INTEGER PRIMARY KEY,
                   channel_id INTEGER
                   )
        """)
    
    conn.commit()
    conn.close()