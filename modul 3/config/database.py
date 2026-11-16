import os

import mysql.connector

class Database:
    def __init__(self):
        self.host = os.getenv("MYSQL_HOST", "localhost")
        self.user = os.getenv("MYSQL_USER", "root")
        self.password = os.getenv("MYSQL_PASSWORD", "")
        self.database = os.getenv("MYSQL_DATABASE", "perpustakaan")
        self.port = int(os.getenv("MYSQL_PORT", "3306"))

    def connect(self):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            return conn
        except mysql.connector.Error as err:
            print(f"Koneksi gagal: {err}")
            return None