import sys
from pathlib import Path

import mysql.connector

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config.database import Database

class AnggotaModel:
    def __init__(self):
        # Inisialisasi koneksi database
        self.db = Database()
        self.table_name = "anggota"

    def get_all_anggota(self):
        conn = self.db.connect()
        if conn is None:
            return []

        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                f"SELECT id_anggota, nama, alamat "
                f"FROM {self.table_name} ORDER BY id_anggota"
            )
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Gagal mengambil data anggota: {err}")
            return []
        finally:
            if cursor is not None:
                cursor.close()
            conn.close()

    def create_anggota(self, nama, alamat):
        conn = self.db.connect()
        if conn is None:
            return False

        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(
                f"INSERT INTO {self.table_name} (nama, alamat) VALUES (%s, %s)",
                (nama, alamat),
            )
            conn.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            conn.rollback()
            print(f"Gagal menambah anggota: {err}")
            return False
        finally:
            if cursor is not None:
                cursor.close()
            conn.close()

    def update_anggota(self, id_anggota, nama, alamat):
        conn = self.db.connect()
        if conn is None:
            return False

        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE anggota SET nama=%s, alamat=%s WHERE id_anggota=%s",
                (nama, alamat, id_anggota),
            )
            conn.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            conn.rollback()
            print(f"Gagal memperbarui anggota: {err}")
            return False
        finally:
            if cursor is not None:
                cursor.close()
            conn.close()

    def delete_anggota(self, id_anggota):
        conn = self.db.connect()
        if conn is None:
            return False

        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM anggota WHERE id_anggota=%s", (id_anggota,)
            )
            conn.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            conn.rollback()
            print(f"Gagal menghapus anggota: {err}")
            return False
        finally:
            if cursor is not None:
                cursor.close()
            conn.close()


if __name__ == "__main__":
    data_anggota = AnggotaModel().get_all_anggota()
    if data_anggota:
        for anggota in data_anggota:
            print(anggota)
    else:
        print("Belum ada data anggota.")