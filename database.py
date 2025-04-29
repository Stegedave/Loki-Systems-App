# loki systems database

import sqlite3

def create_database():
    conn = sqlite3.connect('leethal.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS services (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              date TEXT,
              time TEXT,
              service_provided TEXT,
              service_fee TEXT,
              service_notes TEXT
              )
         ''')
    conn.commit()
    conn.close()


def save_service_record(data):
    conn = sqlite3.connect('leethal.db')
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
    conn = sqlite3.connect('leethal.db')
    c = conn.cursor()
    c.execute('SELECT * FROM services')
    
    services = c.fetchall()
    
    conn.close()
    return services


def delete_service(service_id):
    conn = sqlite3.connect('leethal.db')
    c = conn.cursor()
    c.execute('DELETE FROM services WHERE id = ?', (service_id,))
    conn.commit()
    conn.close()


