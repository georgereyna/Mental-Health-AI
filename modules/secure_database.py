import sqlite3
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import json

class SecureDatabase:
    def __init__(self, db_file='patient_records.db', key=None):
        self.db_file = db_file
        self.key = key if key else get_random_bytes(32)  # Use a provided key or generate a new one
        self.conn = None
        self.create_database()

    def create_database(self):
        self.conn = sqlite3.connect(self.db_file)
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients
        (id TEXT PRIMARY KEY, data TEXT)
        ''')
        self.conn.commit()

    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_ECB)
        # Convert dict to JSON string, then encode to bytes
        json_data = json.dumps(data)
        return cipher.encrypt(pad(json_data.encode(), AES.block_size))

    def decrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_ECB)
        decrypted_data = unpad(cipher.decrypt(data), AES.block_size).decode()
        # Convert JSON string back to dict
        return json.loads(decrypted_data)

    def insert_patient(self, patient_id, data):
        encrypted_data = self.encrypt(data)
        cursor = self.conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO patients (id, data) VALUES (?, ?)",
                       (patient_id, encrypted_data))
        self.conn.commit()

    def get_patient(self, patient_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT data FROM patients WHERE id = ?", (patient_id,))
        result = cursor.fetchone()
        if result:
            return self.decrypt(result[0])
        return None

    def close(self):
        if self.conn:
            self.conn.close()

    def __del__(self):
        self.close()