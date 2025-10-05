# database_tools.py - Untuk menyimpan history chat
import sqlite3
import json
from datetime import datetime

def init_db():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chats
                 (id INTEGER PRIMARY KEY, timestamp TEXT, query TEXT, response TEXT, language TEXT)''')
    conn.commit()
    conn.close()

def save_chat(query, response, language):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("INSERT INTO chats (timestamp, query, response, language) VALUES (?, ?, ?, ?)",
              (datetime.now().isoformat(), query, response, language))
    conn.commit()
    conn.close()

def get_chat_history(limit=10):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("SELECT * FROM chats ORDER BY timestamp DESC LIMIT ?", (limit,))
    results = c.fetchall()
    conn.close()
    return results