"""test_member2.py - run this to test your screens before Member 1's dashboard is ready.

    python test_member2.py

Member 1's dashboard will later do the same thing:
    from books_ui import BooksFrame
    from members_ui import MembersFrame
"""
import tkinter as tk
from tkinter import ttk

from books_ui import BooksFrame
from members_ui import MembersFrame

root = tk.Tk()
root.title("Library Management System - Member 2 Test")
root.geometry("900x600")

tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True)
tabs.add(BooksFrame(tabs), text="Books")
tabs.add(MembersFrame(tabs), text="Members")

root.mainloop()