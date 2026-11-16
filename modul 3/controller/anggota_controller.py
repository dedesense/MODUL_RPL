import tkinter.messagebox as messagebox

from models.anggota_model import AnggotaModel


class AnggotaController:
    def __init__(self, view):
        self.model = AnggotaModel()
        self.view = view
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_update.configure(command=self.update_data)
        self.view.btn_delete.configure(command=self.hapus_data)
        self.view.tabel_anggota.bind("<<TreeviewSelect>>", self.pilih_data)
        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel_anggota.get_children():
            self.view.tabel_anggota.delete(item)

        for anggota in self.model.get_all_anggota():
            self.view.tabel_anggota.insert(
                "",
                "end",
                values=(
                    anggota["id_anggota"],
                    anggota["nama"],
                    anggota["alamat"] or "",
                ),
            )

    def pilih_data(self, _event=None):
        selection = self.view.tabel_anggota.selection()
        if not selection:
            return

        values = self.view.tabel_anggota.item(selection[0], "values")
        for entry, value in (
            (self.view.entry_nama, values[1]),
            (self.view.entry_alamat, values[2]),
        ):
            entry.delete(0, "end")
            entry.insert(0, value)

    def _selected_id(self):
        selection = self.view.tabel_anggota.selection()
        if not selection:
            messagebox.showwarning(
                "Peringatan",
                "Pilih data anggota terlebih dahulu.",
                parent=self.view.winfo_toplevel(),
            )
            return None
        return int(self.view.tabel_anggota.item(selection[0], "values")[0])

    def _form_data(self):
        nama = self.view.entry_nama.get().strip()
        alamat = self.view.entry_alamat.get().strip()
        if not nama:
            messagebox.showwarning(
                "Peringatan",
                "Nama anggota harus diisi.",
                parent=self.view.winfo_toplevel(),
            )
            return None
        return nama, alamat

    def simpan_data(self):
        data = self._form_data()
        if data is None:
            return
        if self.model.create_anggota(*data):
            messagebox.showinfo(
                "Sukses",
                "Data anggota berhasil disimpan.",
                parent=self.view.winfo_toplevel(),
            )
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error",
                "Data anggota gagal disimpan. Periksa koneksi Laragon.",
                parent=self.view.winfo_toplevel(),
            )

    def update_data(self):
        id_anggota = self._selected_id()
        if id_anggota is None:
            return
        data = self._form_data()
        if data is None:
            return
        if self.model.update_anggota(id_anggota, *data):
            self.bersihkan_form()
            self.muat_data_tabel()
            messagebox.showinfo(
                "Sukses",
                "Data anggota berhasil diperbarui.",
                parent=self.view.winfo_toplevel(),
            )
        else:
            messagebox.showerror(
                "Error",
                "Data anggota gagal diperbarui.",
                parent=self.view.winfo_toplevel(),
            )

    def hapus_data(self):
        id_anggota = self._selected_id()
        if id_anggota is None:
            return
        confirmed = messagebox.askyesno(
            "Konfirmasi",
            "Hapus anggota yang dipilih?",
            parent=self.view.winfo_toplevel(),
        )
        if not confirmed:
            return
        if self.model.delete_anggota(id_anggota):
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error",
                "Data anggota gagal dihapus. Anggota mungkin masih terkait dengan peminjaman.",
                parent=self.view.winfo_toplevel(),
            )

    def bersihkan_form(self):
        self.view.entry_nama.delete(0, "end")
        self.view.entry_alamat.delete(0, "end")