import customtkinter as ctk
from tkinter import ttk


BACKGROUND = "#180a08"
PANEL = "#35150f"
PANEL_LIGHT = "#542219"
FIELD = "#1c0c09"
BORDER = "#a44227"
TEXT = "#ffe6b5"
MUTED_TEXT = "#c99368"
ACCENT = "#d44426"
ACCENT_HOVER = "#fa6035"
HIGHLIGHT = "#ffc24f"
GLOW = "#b34cce"
FONT_NAME = "Lucida Console"


def add_pixel_rule(master, padx=16, row=None):
    rule = ctk.CTkFrame(master, fg_color="transparent", height=7, corner_radius=0)
    if row is None:
        rule.pack(fill="x", padx=padx, pady=(0, 12))
    else:
        rule.grid(row=row, column=0, padx=padx, pady=(0, 12), sticky="ew")
    rule.pack_propagate(False)

    for color in (ACCENT, HIGHLIGHT, GLOW, ACCENT_HOVER):
        ctk.CTkFrame(rule, fg_color=color, corner_radius=0).pack(
            side="left",
            fill="both",
            expand=True,
        )


def style_treeview(master):
    style = ttk.Style(master)
    if "clam" in style.theme_names():
        style.theme_use("clam")

    style.configure(
        "Retro.Treeview",
        background=FIELD,
        fieldbackground=FIELD,
        foreground=TEXT,
        rowheight=35,
        borderwidth=0,
        font=(FONT_NAME, 10),
    )
    style.map(
        "Retro.Treeview",
        background=[("selected", GLOW)],
        foreground=[("selected", "#ffffff")],
    )
    style.configure(
        "Retro.Treeview.Heading",
        background=PANEL_LIGHT,
        foreground=HIGHLIGHT,
        font=(FONT_NAME, 10, "bold"),
        padding=(10, 9),
        relief="flat",
    )
    style.map(
        "Retro.Treeview.Heading",
        background=[("active", BORDER)],
        foreground=[("active", TEXT)],
    )
