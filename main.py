"""
main.py - Master Integrated Desktop Application
College Library Management & Fine Tracking System

Consolidates:
  - Member 1: Database Architecture & Shared Configuration (db_config.py)
  - Member 2: Books Inventory (books_ui.py) & Member Directory (members_ui.py)
  - Member 3: Circulation, Borrowing & Fine Management (circulation_ui.py)
  - Member 4: Analytics, Views & Defaulter Reports (app.py)
"""

import tkinter as tk
from tkinter import ttk, messagebox

# Import team module frames
from books_ui import BooksFrame
from members_ui import MembersFrame
from circulation_ui import CirculationFrame
from app import DashboardFrame


class MasterLibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("College Library Management & Fine Tracking System")
        self.geometry("1200x780")
        self.minsize(1050, 700)
        self.configure(bg="#f8fafc")

        # TTK Theme & Global Styles
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        
        # Primary Navigation Tabs Styling
        self.style.configure(
            "TNotebook.Tab", 
            font=("Segoe UI", 10, "bold"), 
            padding=[16, 8],
            background="#e2e8f0",
            foreground="#334155"
        )
        self.style.map(
            "TNotebook.Tab", 
            background=[("selected", "#0f172a")], 
            foreground=[("selected", "#ffffff")]
        )

        # Treeview / Table Global Styling
        self.style.configure(
            "Treeview", 
            font=("Segoe UI", 9), 
            rowheight=26, 
            background="#ffffff", 
            fieldbackground="#ffffff"
        )
        self.style.configure(
            "Treeview.Heading", 
            font=("Segoe UI", 9, "bold"), 
            background="#1e293b", 
            foreground="#ffffff"
        )
        self.style.map("Treeview", background=[("selected", "#cbd5e1")])

        # Top Master Header Banner
        header = tk.Frame(self, bg="#0f172a", height=55)
        header.pack(fill="x")

        tk.Label(
            header,
            text="🏛️ College Library Management & Fine Tracking System",
            font=("Segoe UI", 15, "bold"),
            fg="#f8fafc",
            bg="#0f172a"
        ).pack(side="left", padx=20, pady=12)

        tk.Label(
            header,
            text="Centralized Circulation, Inventory & Defaulters Portal",
            font=("Segoe UI", 9),
            fg="#94a3b8",
            bg="#0f172a"
        ).pack(side="right", padx=20, pady=16)

        # Primary Multi-Module Navigation Notebook
        self.nav_tabs = ttk.Notebook(self)
        self.nav_tabs.pack(fill="both", expand=True)

        # Tab 1: Books Inventory (Member 2)
        self.books_tab = BooksFrame(self.nav_tabs)
        self.nav_tabs.add(self.books_tab, text=" 📚 Books Inventory ")

        # Tab 2: Members Directory (Member 2)
        self.members_tab = MembersFrame(self.nav_tabs)
        self.nav_tabs.add(self.members_tab, text=" 👥 Member Directory ")

        # Tab 3: Circulation & Fines (Member 3)
        self.circulation_tab = CirculationFrame(self.nav_tabs)
        self.nav_tabs.add(self.circulation_tab, text=" 🔄 Circulation & Returns ")

        # Tab 4: Analytics, Views & Reports (Member 4 - You)
        self.analytics_tab = DashboardFrame(self.nav_tabs)
        self.nav_tabs.add(self.analytics_tab, text=" 📈 Reports & Analytics ")

        # Auto-refresh active tab tables upon navigation
        self.nav_tabs.bind("<<NotebookTabChanged>>", self._on_tab_change)

    def _on_tab_change(self, event):
        """Refreshes table views dynamically when clicking across tabs."""
        try:
            selected_text = self.nav_tabs.tab(self.nav_tabs.select(), "text")
            
            if "Reports & Analytics" in selected_text:
                self.analytics_tab.load_all_data()
            elif "Books Inventory" in selected_text:
                self.books_tab.load_books()
            elif "Member Directory" in selected_text:
                self.members_tab.load_members()
            elif "Circulation & Returns" in selected_text:
                if hasattr(self.circulation_tab, "refresh_return_table"):
                    self.circulation_tab.refresh_return_table()
                if hasattr(self.circulation_tab, "refresh_fines_table"):
                    self.circulation_tab.refresh_fines_table()
        except Exception:
            # Prevents UI freeze if switching tabs while a query is running
            pass


if __name__ == "__main__":
    app = MasterLibraryApp()
    app.mainloop()