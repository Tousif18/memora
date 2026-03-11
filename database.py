import sqlite3

conn = sqlite3.connect("memora.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    note TEXT
)
""")

conn.commit()


def save_memory(note):
    cursor.execute("INSERT INTO memory (note) VALUES (?)", (note,))
    conn.commit()


def get_memories():
    cursor.execute("SELECT * FROM memory")
    return cursor.fetchall()

cursor.execute("""
CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT,
    reminder_time TEXT
)
""")

conn.commit()
def save_reminder(task, reminder_time):
    cursor.execute(
        "INSERT INTO reminders (task, reminder_time) VALUES (?, ?)",
        (task, reminder_time)
    )
    conn.commit()


def get_reminders():
    cursor.execute("SELECT * FROM reminders")
    return cursor.fetchall()

cursor.execute("""
CREATE TABLE IF NOT EXISTS moods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mood TEXT
)
""")

conn.commit()    
def save_mood(mood):
    cursor.execute("INSERT INTO moods (mood) VALUES (?)", (mood,))
    conn.commit()


def get_moods():
    cursor.execute("SELECT * FROM moods")
    return cursor.fetchall()

cursor.execute("""
CREATE TABLE IF NOT EXISTS emergency (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alert TEXT
)
""")

conn.commit()

def save_emergency(alert):
    cursor.execute("INSERT INTO emergency (alert) VALUES (?)", (alert,))
    conn.commit()


def get_emergency():
    cursor.execute("SELECT * FROM emergency")
    return cursor.fetchall()