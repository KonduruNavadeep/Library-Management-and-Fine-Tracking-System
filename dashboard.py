"""
dashboard.py - the main window shown after a successful login.

Left side: navigation menu. Right side: the screen for the chosen module.
Until a teammate's screen is ready, the menu item shows a "coming soon" page.
"""

import tkinter as tk
from tkinter import messagebox

# Teammates plug their screens in here. A screen is any tk.Frame subclass whose
# constructor takes the parent frame as its only argument. For example:
#     from inventory_ui import BooksPage
#     PAGE_BUILDERS["Books"] = BooksPage
PAGE_BUILDERS = {}

HEADER_COLOR = "#1f3a5f"
SIDEBAR_COLOR = "#e8edf3"

MENU_ITEMS = ["Home", "Books", "Members", "Issue / Return", "Fines", "Reports"]
ADMIN_ONLY_ITEMS = ["Users"]


class PlaceholderPage(tk.Frame):
    def __init__(self, parent, title):
        super().__init__(parent)
        tk.Label(self, text=title, font=("Helvetica", 20, "bold")).pack(pady=(50, 10))
        tk.Label(self, text="This screen is coming soon.").pack()


class HomePage(tk.Frame):
    def __init__(self, parent, username, role):
        super().__init__(parent)
        tk.Label(self, text=f"Welcome, {username}", font=("Helvetica", 20, "bold")).pack(pady=(50, 10))
        tk.Label(self, text=f"You are logged in as {role}.").pack()
        tk.Label(self, text="Choose a module from the menu on the left.").pack(pady=10)


class Dashboard(tk.Tk):
    def __init__(self, username, role):
        super().__init__()
        self.username = username
        self.role = role
        self.logged_out = False      # True only when the Logout button was used

        self.title("Library Management System")
        self.geometry("900x560")
        self.minsize(700, 450)

        self._build_header()
        self._build_body()
        self.show_page("Home")

    def _build_header(self):
        header = tk.Frame(self, bg=HEADER_COLOR)
        header.pack(fill="x")
        tk.Label(header, text="Library Management System", bg=HEADER_COLOR, fg="white",
                 font=("Helvetica", 16, "bold")).pack(side="left", padx=15, pady=12)
        tk.Label(header, text=f"{self.username} ({self.role})", bg=HEADER_COLOR,
                 fg="white").pack(side="right", padx=15)

    def _build_body(self):
        body = tk.Frame(self)
        body.pack(fill="both", expand=True)

        sidebar = tk.Frame(body, width=180, bg=SIDEBAR_COLOR)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Button(sidebar, text="Logout", command=self.logout).pack(
            side="bottom", fill="x", padx=10, pady=15)

        items = list(MENU_ITEMS)
        if self.role == "Admin":
            items += ADMIN_ONLY_ITEMS
        for name in items:
            tk.Button(sidebar, text=name, command=lambda n=name: self.show_page(n)).pack(
                fill="x", padx=10, pady=3)

        # The page for the chosen module is drawn in here
        self.content = tk.Frame(body)
        self.content.pack(side="right", fill="both", expand=True)

    def show_page(self, name):
        if name in ADMIN_ONLY_ITEMS and self.role != "Admin":
            messagebox.showerror("Access denied", "Only an Admin can open this page.")
            return

        for widget in self.content.winfo_children():     # clear the old page
            widget.destroy()

        if name == "Home":
            page = HomePage(self.content, self.username, self.role)
        elif name in PAGE_BUILDERS:
            page = PAGE_BUILDERS[name](self.content)
        else:
            page = PlaceholderPage(self.content, name)
        page.pack(fill="both", expand=True)

    def logout(self):
        if messagebox.askyesno("Logout", "Do you want to log out?"):
            self.logged_out = True
            self.destroy()
if __name__ == "__main__":
    # Passing dummy credentials to test the UI
    app = Dashboard(username="TestUser", role="Admin")
    app.mainloop()