"""
login.py - the login window for Admin and Librarian users.

After a successful login, self.user holds {"username": ..., "role": ...}
and the window closes. If the window is closed without logging in,
self.user stays None. main.py decides what to open next.
"""

import tkinter as tk

import bcrypt
import mysql.connector

from db_config import get_connection
from validators import is_not_empty


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.user = None

        self.title("Library Management System - Login")
        self.geometry("380x320")
        self.resizable(False, False)

        tk.Label(self, text="Library System", font=("Helvetica", 20, "bold")).pack(pady=(30, 4))
        tk.Label(self, text="Admin / Librarian login").pack(pady=(0, 18))

        form = tk.Frame(self)
        form.pack()

        tk.Label(form, text="Username").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        self.username_entry = tk.Entry(form, width=24)
        self.username_entry.grid(row=0, column=1, pady=6)

        tk.Label(form, text="Password").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        self.password_entry = tk.Entry(form, width=24, show="*")
        self.password_entry.grid(row=1, column=1, pady=6)

        self.error_label = tk.Label(self, text="", fg="red")
        self.error_label.pack(pady=(12, 0))

        tk.Button(self, text="Login", width=14, command=self.attempt_login).pack(pady=12)

        self.bind("<Return>", lambda event: self.attempt_login())   # Enter key logs in
        self.username_entry.focus()

    def attempt_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        # 1. Both boxes must be filled
        for value, name in ((username, "Username"), (password, "Password")):
            ok, _ = is_not_empty(value)
            if not ok:
                self.error_label.config(text=f"{name} cannot be empty.")
                return

        # 2. Look the user up
        try:
            row = self.find_user(username)
        except mysql.connector.Error:
            self.error_label.config(text="Cannot connect to the database.")
            return

        # 3. Same message for a wrong username and a wrong password
        if row is None or not self.password_matches(password, row["password"]):
            self.error_label.config(text="Invalid username or password.")
            self.password_entry.delete(0, tk.END)
            return

        # 4. Success: remember who logged in and close this window
        self.user = {"username": row["username"], "role": row["role"]}
        self.destroy()

    @staticmethod
    def find_user(username):
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            # The username goes in as a parameter, never joined into the SQL text
            cur.execute(
                "SELECT user_id, username, password, role FROM Users WHERE username = %s",
                (username,),
            )
            return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def password_matches(typed, stored_hash):
        try:
            return bcrypt.checkpw(typed.encode(), stored_hash.encode())
        except ValueError:
            # Stored value is not a bcrypt hash (for example plain text), or the password is too long
            return False
if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
