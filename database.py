# loki systems database

import sqlite3
import sqlite3
import os

def get_db_path():
    appdata = os.getenv("APPDATA")
    db_dir = os.path.join(appdata, "LokiSystems")
    os.makedirs(db_dir, exist_ok=True)
    return os.path.join(db_dir, "leethal.db")

def create_database():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            time TEXT,
            service_provided TEXT,
            service_fee REAL,
            service_notes TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_service_record(data):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        INSERT INTO services (date, time, service_provided, service_fee, service_notes)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        data["Date (YYYY-MM-DD)"],
        data["Time (HH:MM)"],
        data["Service Provided"],
        data["Service Fee"],
        data["Service Notes"]
    ))
    conn.commit()
    conn.close()

def fetch_all_services():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM services")
    services = c.fetchall()
    conn.close()
    return services

def delete_service(service_id):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM services WHERE id=?", (service_id,))
    conn.commit()
    conn.close()



