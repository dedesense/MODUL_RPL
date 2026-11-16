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
    GLOW,
    HIGHLIGHT,
    MUTED_TEXT,
    PANEL,
    PANEL_LIGHT,
    TEXT,
    add_pixel_rule,
    style_treeview,
)


class BukuView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=BACKGROUND, corner_radius=0)

        self.grid_columnconfigure(0, weight=1, minsize=270)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        self.frame_kiri = ctk.CTkFrame(
            self,
            fg_color=PANEL,
            border_width=2,
            border_color=ACCENT,
            corner_radius=0,
        )
        self.frame_kiri.grid(row=0, column=0, padx=(0, 8), pady=8, sticky="nsew")

        ctk.CTkLabel(
            self.frame_kiri,
            text="FORM DATA BUKU",
            text_color=HIGHLIGHT,
            font=(FONT_NAME, 14, "bold"),
        ).pack(pady=(22, 16))
        add_pixel_rule(self.frame_kiri)

        input_style = {
            "fg_color": FIELD,
            "text_color": TEXT,
            "placeholder_text_color": MUTED_TEXT,
            "border_color": BORDER,
            "border_width": 2,
            "corner_radius": 0,
            "height": 38,
            "font": (FONT_NAME, 10),
        }
        self.entry_judul = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Masukkan Judul Buku",
            **input_style,
        )
        self.entry_judul.pack(pady=8, padx=16, fill="x")

        self.entry_penulis = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Masukkan Nama Penulis",
            **input_style,
        )
        self.entry_penulis.pack(pady=8, padx=16, fill="x")

        self.entry_tahun = ctk.CTkEntry(
            self.frame_kiri,
            placeholder_text="Tahun Terbit (Misal: 2024)",
            **input_style,
        )
        self.entry_tahun.pack(pady=8, padx=16, fill="x")

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
        self.btn_simpan.pack(pady=(18, 8), padx=16, fill="x")

        self.btn_perbarui = ctk.CTkButton(
            self.frame_kiri,
            text="Perbarui Data (Update)",
            fg_color=PANEL_LIGHT,
            hover_color=BORDER,
            border_width=2,
            border_color=HIGHLIGHT,
            **button_style,
        )
        self.btn_perbarui.pack(pady=8, padx=16, fill="x")

        self.btn_hapus = ctk.CTkButton(
            self.frame_kiri,
            text="Hapus Data (Delete)",
            fg_color="#743222",
            hover_color=ACCENT_HOVER,
            border_width=2,
            border_color=HIGHLIGHT,
            **button_style,
        )
        self.btn_hapus.pack(pady=8, padx=16, fill="x")

        self.btn_logout = ctk.CTkButton(
            self.frame_kiri,
            text="Logout",
            fg_color=BACKGROUND,
            hover_color=GLOW,
            border_width=2,
            border_color=GLOW,
            **button_style,
        )
        self.btn_logout.pack(side="bottom", pady=16, padx=16, fill="x")

        self.frame_kanan = ctk.CTkFrame(
            self,
            fg_color=PANEL,
            border_width=2,
            border_color=ACCENT,
            corner_radius=0,
        )
        self.frame_kanan.grid(row=0, column=1, padx=(8, 0), pady=8, sticky="nsew")

        ctk.CTkLabel(
            self.frame_kanan,
            text="DAFTAR KOLEKSI BUKU",
            text_color=HIGHLIGHT,
            font=(FONT_NAME, 14, "bold"),
        ).pack(pady=(22, 12))
        add_pixel_rule(self.frame_kanan)

        kolom = ("id", "judul", "penulis", "tahun")
        style_treeview(self)
        self.tabel = ttk.Treeview(
            self.frame_kanan,
            columns=kolom,
            show="headings",
            height=15,
            style="Retro.Treeview",
        )

        self.tabel.heading("id", text="ID")
        self.tabel.heading("judul", text="JUDUL BUKU")
        self.tabel.heading("penulis", text="PENULIS")
        self.tabel.heading("tahun", text="TAHUN")

        self.tabel.column("id", width=40, anchor="center")
        self.tabel.column("judul", width=220)
        self.tabel.column("penulis", width=180)
        self.tabel.column("tahun", width=90, anchor="center")

        self.tabel.pack(fill="both", expand=True, padx=16, pady=(0, 16))

if __name__ == "__main__":
    from controller.buku_controller import BukuController

    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.title("Sistem Manajemen Perpustakaan")
    root.geometry("800x450")
    app = BukuView(root)
    app.pack(fill="both", expand=True)
    controller = BukuController(app)
    root.mainloop()