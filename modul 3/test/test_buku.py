import unittest
from unittest.mock import MagicMock, call, patch

from controller.buku_controller import BukuController
from models.anggota_model import AnggotaModel
from models.buku_model import BukuModel
from models.user_model import UserModel


class ModelDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.cursor = MagicMock()
        self.cursor.rowcount = 1
        self.connection.cursor.return_value = self.cursor

    def make_model(self, model_class):
        model = model_class()
        model.db = MagicMock()
        model.db.connect.return_value = self.connection
        return model

    def test_create_buku(self):
        model = self.make_model(BukuModel)

        self.assertTrue(model.create_buku("Buku Testing", "Penulis QA", 2026))

        self.cursor.execute.assert_called_once_with(
            "INSERT INTO buku (judul, penulis, tahun_terbit) VALUES (%s, %s, %s)",
            ("Buku Testing", "Penulis QA", 2026),
        )
        self.connection.commit.assert_called_once()

    def test_get_all_buku(self):
        model = self.make_model(BukuModel)
        books = [{"id_buku": 1, "judul": "Testing"}]
        self.cursor.fetchall.return_value = books

        self.assertEqual(model.get_all_buku(), books)
        self.cursor.execute.assert_called_once()

    def test_update_and_delete_buku(self):
        model = self.make_model(BukuModel)

        self.assertTrue(model.update_buku(1, "Judul", "Penulis", 2026))
        self.assertTrue(model.delete_buku(1))

        self.assertEqual(self.cursor.execute.call_count, 2)
        self.assertEqual(self.connection.commit.call_count, 2)

    def test_invalid_book_year_does_not_connect(self):
        model = self.make_model(BukuModel)

        self.assertFalse(model.create_buku("Judul", "Penulis", "tahun"))
        model.db.connect.assert_not_called()

    def test_create_anggota(self):
        model = self.make_model(AnggotaModel)

        self.assertTrue(model.create_anggota("Nama", "Alamat"))
        self.cursor.execute.assert_called_once_with(
            "INSERT INTO anggota (nama, alamat) VALUES (%s, %s)",
            ("Nama", "Alamat"),
        )
        self.connection.commit.assert_called_once()

    def test_get_all_anggota(self):
        model = self.make_model(AnggotaModel)
        members = [{"id_anggota": 1, "nama": "Nama", "alamat": "Alamat"}]
        self.cursor.fetchall.return_value = members

        self.assertEqual(model.get_all_anggota(), members)

    def test_update_and_delete_anggota(self):
        model = self.make_model(AnggotaModel)

        self.assertTrue(model.update_anggota(1, "Nama", "Alamat"))
        self.assertTrue(model.delete_anggota(1))

        self.assertEqual(self.cursor.execute.call_count, 2)
        self.assertEqual(self.connection.commit.call_count, 2)

    def test_user_password_hash_and_login(self):
        model = self.make_model(UserModel)
        hashed = model.hash_password("rahasia")

        self.assertEqual(len(hashed), 64)
        self.assertEqual(model.hash_password("rahasia"), hashed)

        self.cursor.fetchone.return_value = {"id": 1, "username": "admin", "role": "admin"}
        self.assertIsNotNone(model.login("admin", "rahasia"))

    def test_user_login_uses_actual_users_table_column_name(self):
        model = self.make_model(UserModel)
        hashed = model.hash_password("rahasia")
        self.cursor.fetchone.return_value = {"id": 1, "username": "admin", "role": "admin"}

        self.assertIsNotNone(model.login("admin", "rahasia"))
        self.cursor.execute.assert_called_once_with(
            "SELECT id_user AS id, username, role FROM users WHERE username = %s AND password = %s",
            ("admin", hashed),
        )

    def test_register_user_hashes_password_before_insert(self):
        model = self.make_model(UserModel)
        self.cursor.lastrowid = 7

        self.assertEqual(model.register_user("anggota1", "rahasia", "anggota"), 7)
        self.cursor.execute.assert_called_once_with(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            ("anggota1", model.hash_password("rahasia"), "anggota"),
        )
        self.connection.commit.assert_called_once()

    @patch("controller.buku_controller.BukuModel")
    def test_anggota_cannot_update_or_delete_books(self, buku_model_class):
        buku_model_class.return_value.get_all_buku.return_value = []
        view = MagicMock()
        view.tabel.get_children.return_value = []

        BukuController(view, user_role="anggota")

        self.assertEqual(view.btn_perbarui.configure.call_args_list[-1], call(state="disabled"))
        self.assertEqual(view.btn_hapus.configure.call_args_list[-1], call(state="disabled"))


if __name__ == "__main__":
    unittest.main()