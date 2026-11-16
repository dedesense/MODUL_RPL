import customtkinter as ctk

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
    TEXT,
    add_pixel_rule,
)


class LoginView(ctk.CTk):
    def __init__(self):
        ctk.set_appearance_mode("dark")
        super().__init__()
        self.configure(fg_color=BACKGROUND)
        self.title("Login Sistem Perpustakaan")
        self.geometry("440x360")
        self.minsize(400, 340)
        self.resizable(False, False)
        self.user = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = ctk.CTkFrame(
            self,
            fg_color=PANEL,
            border_width=2,
            border_color=ACCENT,
            corner_radius=0,
        )
        self.frame.grid(sticky="nsew", padx=24, pady=24)
        self.frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.frame,
            text="LOGIN",
            text_color=HIGHLIGHT,
            font=(FONT_NAME, 24, "bold"),
        ).grid(row=0, column=0, padx=20, pady=(24, 12))
        add_pixel_rule(self.frame, padx=20, row=1)

        label_style = {
            "text_color": TEXT,
            "font": (FONT_NAME, 11, "bold"),
        }
        ctk.CTkLabel(self.frame, text="Username", **label_style).grid(
            row=2, column=0, sticky="w", padx=20, pady=(8, 6)
        )
        input_style = {
            "fg_color": FIELD,
            "text_color": TEXT,
            "placeholder_text_color": MUTED_TEXT,
            "border_color": BORDER,
            "border_width": 2,
            "corner_radius": 0,
            "height": 38,
        }
        self.username_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="Masukkan username",
            **input_style,
        )
        self.username_entry.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(self.frame, text="Password", **label_style).grid(
            row=4, column=0, sticky="w", padx=20, pady=(8, 6)
        )
        self.password_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="Masukkan password",
            show="*",
            **input_style,
        )
        self.password_entry.grid(row=5, column=0, padx=20, pady=(0, 18), sticky="ew")

        self.login_button = ctk.CTkButton(
            self.frame,
            text="Masuk",
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            text_color=TEXT,
            font=(FONT_NAME, 12, "bold"),
            corner_radius=0,
            height=40,
        )
        self.login_button.grid(row=6, column=0, padx=20, pady=(0, 18), sticky="ew")

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.user = None
        self.destroy()


if __name__ == "__main__":
    app = LoginView()
    app.mainloop()
