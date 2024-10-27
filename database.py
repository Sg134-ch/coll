import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("cems.db", check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT,
                date TEXT,
                location TEXT
            )
            """)
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER,
                name TEXT,
                roll_number TEXT,
                email TEXT
            )
            """)
    
    def get_events(self):
        return self.conn.execute("SELECT * FROM events").fetchall()

    def add_event(self, title, description, date, location):
        with self.conn:
            self.conn.execute("INSERT INTO events (title, description, date, location) VALUES (?, ?, ?, ?)", (title, description, date, location))

    def delete_event(self, event_id):
        with self.conn:
            self.conn.execute("DELETE FROM events WHERE id = ?", (event_id,))
            self.conn.execute("DELETE FROM registrations WHERE event_id = ?", (event_id,))

    def register_user(self, event_id, name, roll_number, email):
        with self.conn:
            self.conn.execute("INSERT INTO registrations (event_id, name, roll_number, email) VALUES (?, ?, ?, ?)", (event_id, name, roll_number, email))

    def get_participants(self, event_id):
        return self.conn.execute("SELECT * FROM registrations WHERE event_id = ?", (event_id,)).fetchall()

    def authenticate_admin(self, username, password):
        return username == "admin" and password == "admin123"
