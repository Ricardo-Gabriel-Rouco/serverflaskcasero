import sqlite3

def init_db():
    conn = sqlite3.connect('devices.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT NOT NULL,
            mac TEXT NOT NULL UNIQUE,
            name TEXT,
            last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_device(ip, mac, name=None):
    conn = sqlite3.connect('devices.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO devices (ip, mac, name)
        VALUES (?, ?, ?)
    ''', (ip, mac, name))
    conn.commit()
    conn.close()
    
def get_all_devices():
    conn = sqlite3.connect('devices.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM devices')
    devices = cursor.fetchall()
    conn.close()
    return devices
