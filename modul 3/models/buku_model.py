import mysql.connector

from config.database import Database


class BukuModel:
    def __init__(self):
        self.db = Database()
        self.table_name = "buku"

    def get_all_buku(self):
        conn = self.db.connect()
        if conn is None:
            return []

        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT id_buku, judul, penulis, tahun_terbit "
                f"FROM {self.table_name} ORDER BY id_buku"
            )
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Gagal mengambil data buku: {err}")
            return []
        finally:
            if cursor is not None:
                cursor.close()
            conn.close()

    def create_buku(self, judul, penulis, tahun_terbit):
        try:
            tahun_terbit = int(tahun_terbit)
        except (TypeError, ValueError):
            return False

        conn = self.db.connect()
        if conn is None:
            return False

        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(
                f"INSERT INTO {self.table_name} (judul, penulis, tahun_terbit) "
                "VALUES (%s, %s, %s)",
                (judul, penulis, tahun_terbit),
            )
            conn.commit()
            return cursor.lastrowid if cursor.rowcount > 0 else False
        except mysql.connector.Error as err:
            conn.rollback()
            print(f"Gagal menambah data buku: {err}")
            return False
        finally:
            if cursor is not None:
                cursor.close()
            conn.close()

    def update_buku(self, id_buku, judul, penulis, tahun_terbit):
        try:
            tahun_terbit = int(tahun_terbit)
        except (TypeError, ValueError):
            return False

        conn = self.db.connect()
        if conn is None:
            return False

        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(
                f"""
                    UPDATE {self.table_name}
                    SET judul = %s,
                        penulis = %s,
                        tahun_terbit = %s
                    WHERE id_buku = %s
                """,
                (judul, penulis, tahun_terbit, id_buku),
            )
            conn.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            conn.rollback()
            print(f"Gagal memperbarui data buku: {err}")
            return False
        finally:
            if cursor is not None:
                cursor.close()
            conn.close()

    def delete_buku(self, id_buku):
        conn = self.db.connect()
        if conn is None:
            return False

        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(
                f"""
                    DELETE FROM {self.table_name}
                    WHERE id_buku = %s
                """,
                (id_buku,),
            )
            conn.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            conn.rollback()
            print(f"Gagal menghapus data buku: {err}")
            return False
        finally:
            if cursor is not None:
                cursor.close()
            conn.close()

    def tambah_buku(self, judul, penulis, tahun_terbit):
        return self.create_buku(judul, penulis, tahun_terbit)

    def ambil_data_buku(self):
        return self.get_all_buku()

    def hapus_buku(self, id_buku):
        return self.delete_buku(id_buku)