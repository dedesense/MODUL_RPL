import hashlib
import sys
from pathlib import Path

import mysql.connector

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config.database import Database


class UserModel:
    def __init__(self):
        self.db = Database()
        self.table_name = "users"

    def hash_password(self, password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def register_user(self, username, password, role):
        conn = self.db.connect()
        if conn is None:
            return False

        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(
                f"INSERT INTO {self.table_name} (username, password, role) "
                "VALUES (%s, %s, %s)",
                (username, self.hash_password(password), role),
            )
            conn.commit()
            return cursor.lastrowid if cursor.rowcount > 0 else False
        except mysql.connector.Error as err:
            conn.rollback()
            print(f"Gagal mendaftarkan user: {err}")
            return False
        finally:
            if cursor is not None:
                cursor.close()
            conn.close()

    def login(self, username, password):
        conn = self.db.connect()
        if conn is None:
            return None

        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                f"SELECT id_user AS id, username, role FROM {self.table_name} WHERE username = %s AND password = %s",
                (username, self.hash_password(password)),
            )
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"Gagal login user: {err}")
            return None
        finally:
            if cursor is not None:
                cursor.close()
            conn.close()
