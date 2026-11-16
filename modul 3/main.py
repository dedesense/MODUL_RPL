import sys

import customtkinter as ctk

from controller.anggota_controller import AnggotaController
from controller.auth_controller import AuthController
from controller.buku_controller import BukuController
from views.anggota_view import AnggotaView
from views.buku_view import BukuView
from views.retro_theme import (
    ACCENT,
    BACKGROUND,
    BORDER,
    FONT_NAME,
    GLOW,
    HIGHLIGHT,
    PANEL,
    PANEL_LIGHT,
    TEXT,
    add_pixel_rule,
)


class AplikasiPerpustakaan(ctk.CTk):
    def __init__(self, user_role="admin"):
        super().__init__()
        self.logged_out = False
        ctk.set_appearance_mode("dark")
        self.configure(fg_color=BACKGROUND)
        self.title("Sistem Manajemen Perpustakaan")
        self.geometry("1120x640")
        self.minsize(900, 540)

        self.header = ctk.CTkFrame(
            self,
            fg_color=PANEL,
            border_width=2,
            border_color=BORDER,
            corner_radius=0,
            height=52,
        )
        self.header.pack(fill="x", padx=12, pady=(12, 0))
        self.header.pack_propagate(False)
        ctk.CTkFrame(
            self.header,
            fg_color=ACCENT,
            corner_radius=0,
            width=8,
        ).pack(side="left", fill="y")
        ctk.CTkLabel(
            self.header,
            text="SISTEM PERPUSTAKAAN",
            text_color=HIGHLIGHT,
            font=(FONT_NAME, 15, "bold"),
        ).pack(side="left", padx=14)
        add_pixel_rule(self, padx=12)

        self.tab_view = ctk.CTkTabview(
            self,
            corner_radius=0,
            border_width=2,
            border_color=BORDER,
            fg_color=BACKGROUND,
            segmented_button_fg_color=PANEL,
            segmented_button_selected_color=GLOW,
            segmented_button_selected_hover_color=ACCENT,
            segmented_button_unselected_color=PANEL,
            segmented_button_unselected_hover_color=PANEL_LIGHT,
            text_color=TEXT,
        )
        self.tab_view.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        tab_buku = self.tab_view.add("Buku")
        tab_anggota = self.tab_view.add("Anggota")

        self.buku_view = BukuView(tab_buku)
        self.buku_view.pack(fill="both", expand=True)
        self.anggota_view = AnggotaView(tab_anggota)
        self.anggota_view.pack(fill="both", expand=True)

        self.buku_controller = BukuController(self.buku_view, user_role=user_role)
        self.anggota_controller = AnggotaController(self.anggota_view)
        self.buku_view.btn_logout.configure(command=self.logout)

    def logout(self):
        self.logged_out = True
        self.destroy()


if __name__ == "__main__":
    while True:
        auth_controller = AuthController()
        if not auth_controller.run():
            sys.exit(0)

        app = AplikasiPerpustakaan(user_role=auth_controller.user_role)
        app.mainloop()
        if not app.logged_out:
            break