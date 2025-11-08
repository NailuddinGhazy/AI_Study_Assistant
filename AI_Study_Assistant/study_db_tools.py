# study_db_tools.py
import sqlite3
import os
from datetime import datetime

DB_PATH = "study_assistant.db"

def init_db():
    """Create DB and required tables if not exist."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_message TEXT,
        bot_reply TEXT,
        mode TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS quiz_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        quiz_json TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def save_chat(user_message: str, bot_reply: str, mode: str = "chat"):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO chat_history (user_message, bot_reply, mode, created_at) VALUES (?, ?, ?, ?)",
        (user_message, bot_reply, mode, datetime.now())
    )
    conn.commit()
    conn.close()

def get_recent_chats(limit: int = 20):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM chat_history ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def save_quiz(topic: str, quiz_json: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO quiz_history (topic, quiz_json, created_at) VALUES (?, ?, ?)",
        (topic, quiz_json, datetime.now())
    )
    conn.commit()
    conn.close()

def get_recent_quizzes(limit: int = 20):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM quiz_history ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]
