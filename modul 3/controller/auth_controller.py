import tkinter.messagebox as messagebox

from models.user_model import UserModel
from views.login_view import LoginView


class AuthController:
    def __init__(self):
        self.model = UserModel()
        self.view = LoginView()
        self.user = None
        self.user_role = "guest"
        self.view.login_button.configure(command=self.login)

    def login(self):
        username = self.view.username_entry.get().strip()
        password = self.view.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Peringatan", "Username dan password harus diisi.")
            return False

        user = self.model.login(username, password)
        if user is None:
            messagebox.showerror("Login Gagal", "Username atau password salah.")
            return False

        self.user = user
        self.user_role = user.get("role", "admin")
        self.view.destroy()
        return True

    def run(self):
        self.view.mainloop()
        return self.user is not None
