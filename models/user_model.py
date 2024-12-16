
import sqlite3

class User:
    @staticmethod
    def create_table():
        with sqlite3.connect('users.db') as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                email TEXT UNIQUE NOT NULL,
                                password TEXT NOT NULL
                            )''')

    @staticmethod
    def register(name, email, password):
        try:
            with sqlite3.connect('users.db') as conn:
                conn.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                             (name, email, password))
            return True
        except sqlite3.IntegrityError:
            return False

    @staticmethod
    def authenticate(email, password):
        with sqlite3.connect('users.db') as conn:
            user = conn.execute("SELECT * FROM users WHERE email = ? AND password = ?",
                                (email, password)).fetchone()
        if user:
            return {"id": user[0], "name": user[1], "email": user[2]}
        return None

User.create_table()
