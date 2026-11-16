import tkinter.messagebox as messagebox

from models.buku_model import BukuModel


class BukuController:
    def __init__(self, view, user_role="admin"):
        self.model = BukuModel()
        self.view = view
        self.user_role = str(user_role).lower()
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_hapus.configure(command=self.hapus_data)
        self.view.btn_perbarui.configure(command=self.update_data)
        self.view.tabel.bind("<<TreeviewSelect>>", self.pilih_data)
        self.atur_otorisasi()
        self.muat_data_tabel()

    def atur_otorisasi(self):
        if self.user_role != "admin":
            self.view.btn_simpan.configure(state="disabled")
            self.view.btn_perbarui.configure(state="disabled")
            self.view.btn_hapus.configure(state="disabled")

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        data_buku = self.model.get_all_buku()
        for buku in data_buku:
            self.view.tabel.insert(
                "",
                "end",
                values=(
                    buku["id_buku"],
                    buku["judul"],
                    buku["penulis"],
                    buku["tahun_terbit"],
                ),
            )

    def pilih_data(self, _event=None):
        selection = self.view.tabel.selection()
        if not selection:
            return

        values = self.view.tabel.item(selection[0], "values")
        entries = (
            (self.view.entry_judul, values[1]),
            (self.view.entry_penulis, values[2]),
            (self.view.entry_tahun, values[3]),
        )
        for entry, value in entries:
            entry.delete(0, "end")
            entry.insert(0, value)

    def _selected_id(self):
        selection = self.view.tabel.selection()
        if not selection:
            messagebox.showwarning(
                "Peringatan",
                "Pilih data buku terlebih dahulu.",
                parent=self.view.winfo_toplevel(),
            )
            return None
        return int(self.view.tabel.item(selection[0], "values")[0])

    def _form_data(self):
        judul = self.view.entry_judul.get().strip()
        penulis = self.view.entry_penulis.get().strip()
        tahun = self.view.entry_tahun.get().strip()

        if not judul or not penulis or not tahun:
            messagebox.showwarning(
                "Peringatan",
                "Semua kolom harus diisi.",
                parent=self.view.winfo_toplevel(),
            )
            return None
        if not tahun.isdigit() or not 1901 <= int(tahun) <= 2155:
            messagebox.showwarning(
                "Peringatan",
                "Tahun terbit harus berupa angka antara 1901 dan 2155.",
                parent=self.view.winfo_toplevel(),
            )
            return None
        return judul, penulis, int(tahun)

    def simpan_data(self):
        data = self._form_data()
        if data is None:
            return

        if self.model.create_buku(*data):
            messagebox.showinfo(
                "Sukses",
                "Data buku berhasil disimpan.",
                parent=self.view.winfo_toplevel(),
            )
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error",
                "Data buku gagal disimpan. Periksa koneksi Laragon dan data yang dimasukkan.",
                parent=self.view.winfo_toplevel(),
            )

    def hapus_data(self):
        id_buku = self._selected_id()
        if id_buku is None:
            return

        confirmed = messagebox.askyesno(
            "Konfirmasi",
            "Hapus buku yang dipilih?",
            parent=self.view.winfo_toplevel(),
        )
        if not confirmed:
            return
        if self.model.delete_buku(id_buku):
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error",
                "Data buku gagal dihapus. Buku mungkin masih terkait dengan data peminjaman.",
                parent=self.view.winfo_toplevel(),
            )

    def update_data(self):
        id_buku = self._selected_id()
        if id_buku is None:
            return
        data = self._form_data()
        if data is None:
            return

        if self.model.update_buku(id_buku, *data):
            messagebox.showinfo(
                "Sukses",
                "Data buku berhasil diperbarui.",
                parent=self.view.winfo_toplevel(),
            )
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error",
                "Data buku gagal diperbarui.",
                parent=self.view.winfo_toplevel(),
            )

    def bersihkan_form(self):
        for entry in (
            self.view.entry_judul,
            self.view.entry_penulis,
            self.view.entry_tahun,
        ):
            entry.delete(0, "end")
