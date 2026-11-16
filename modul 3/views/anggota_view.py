import sys
from pathlib import Path

import customtkinter as ctk
from tkinter import ttk

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from views.retro_theme import (
    ACCENT,
    ACCENT_HOVER,
    BACKGROUND,
    BORDER,
    FIELD,
    FONT_NAME,
    HIGHLIGHT,
    MUTED_TEXT,
    PANEL,
    PANEL_LIGHT,
    TEXT,
    add_pixel_rule,
    style_treeview,
)


class AnggotaView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=BACKGROUND, corner_radius=0)

        self.frame_kiri = ctk.CTkFrame(
            self,
            fg_color=PANEL,
            border_width=2,
            border_color=ACCENT,
            corner_radius=0,
        )
        self.frame_kiri.pack(side="left", fill="y", padx=(0, 8), pady=8)

        self.lbl_judul_form = ctk.CTkLabel(
            self.frame_kiri,
            text="FORM DATA ANGGOTA",
            text_color=HIGHLIGHT,
            font=(FONT_NAME, 13, "bold"),
        )
        self.lbl_judul_form.pack(pady=(22, 16), padx=16)
        add_pixel_rule(self.frame_kiri)

        input_style = {
            "fg_color": FIELD,
            "text_color": TEXT,
            "placeholder_text_color": MUTED_TEXT,
            "border_color": BORDER,
            "border_width": 2,
            "corner_radius": 0,
            "height": 38,
            "width": 250,
            "font": (FONT_NAME, 10),
        }
        self.entry_nama = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Masukkan Nama Anggota",
            **input_style,
        )
        self.entry_nama.pack(pady=8, padx=16)

        self.entry_alamat = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Masukkan Alamat",
            **input_style,
        )
        self.entry_alamat.pack(pady=(8, 20), padx=16)

        button_style = {
            "text_color": TEXT,
            "corner_radius": 0,
            "height": 38,
            "font": (FONT_NAME, 10, "bold"),
        }
        self.btn_simpan = ctk.CTkButton(
            self.frame_kiri,
            text="Simpan Data",
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            border_width=2,
            border_color=HIGHLIGHT,
            **button_style,
        )
        self.btn_simpan.pack(pady=8, padx=16, fill="x")

        self.btn_update = ctk.CTkButton(
            self.frame_kiri,
            text="Perbarui Data (Update)",
            fg_color=PANEL_LIGHT,
            hover_color=BORDER,
            border_width=2,
            border_color=HIGHLIGHT,
            **button_style,
        )
        self.btn_update.pack(pady=8, padx=16, fill="x")

        self.btn_delete = ctk.CTkButton(
            self.frame_kiri,
            text="Hapus Data (Delete)",
            fg_color="#743222",
            hover_color=ACCENT_HOVER,
            border_width=2,
            border_color=HIGHLIGHT,
            **button_style,
        )
        self.btn_delete.pack(pady=8, padx=16, fill="x")

        self.frame_kanan = ctk.CTkFrame(
            self,
            fg_color=PANEL,
            border_width=2,
            border_color=ACCENT,
            corner_radius=0,
        )
        self.frame_kanan.pack(side="right", fill="both", expand=True, padx=(8, 0), pady=8)

        self.lbl_judul_tabel = ctk.CTkLabel(
            self.frame_kanan,
            text="DAFTAR ANGGOTA PERPUSTAKAAN",
            text_color=HIGHLIGHT,
            font=(FONT_NAME, 13, "bold"),
        )
        self.lbl_judul_tabel.pack(pady=(22, 12))
        add_pixel_rule(self.frame_kanan)

        style_treeview(self)

        kolom_tabel = ("id_anggota", "nama", "alamat")
        self.tabel_anggota = ttk.Treeview(
            self.frame_kanan,
            columns=kolom_tabel,
            show="headings",
            height=15,
            style="Retro.Treeview",
        )
        
        self.tabel_anggota.heading("id_anggota", text="ID")
        self.tabel_anggota.column("id_anggota", width=50, anchor="center")

        self.tabel_anggota.heading("nama", text="NAMA ANGGOTA")
        self.tabel_anggota.column("nama", width=250, anchor="w")

        self.tabel_anggota.heading("alamat", text="ALAMAT")
        self.tabel_anggota.column("alamat", width=300, anchor="w")

        self.tabel_anggota.pack(fill="both", expand=True, padx=16, pady=(0, 16))

if __name__ == "__main__":
    from controller.anggota_controller import AnggotaController

    root = ctk.CTk()
    root.title("Sistem Manajemen Perpustakaan - Data Anggota")
    root.geometry("900x500")
    ctk.set_appearance_mode("dark")
    app = AnggotaView(root)
    app.pack(fill="both", expand=True)
    controller = AnggotaController(app)
    root.mainloop()