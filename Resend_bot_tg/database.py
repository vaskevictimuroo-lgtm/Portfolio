#database.py

import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        moderator_chat_message_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        user_message_id TEXT NOT NULL)
    ''')
    conn.commit()
    conn.close()
def save_link(moderator_chat_message_id, user_id, user_message_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO users (moderator_chat_message_id, user_id, user_message_id)
        VALUES (?, ?, ?)
    ''', (moderator_chat_message_id, user_id, user_message_id))
    conn.commit()
    conn.close()

def give_link(moderator_chat_message_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''SELECT user_id, user_message_id FROM users
                 WHERE moderator_chat_message_id = ?''', (moderator_chat_message_id,))
    result = c.fetchone()
    conn.close()

    if result is None:
        return None
    else:
        user_id, user_message_id = result
        return user_id, user_message_id

