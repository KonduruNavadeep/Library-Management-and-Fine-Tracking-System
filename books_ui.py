"""books_ui.py - Book Management screen: Insert, View, Update, Delete + Search (Member 2)."""
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

from db_config import get_connection      # written by Member 1
from inventory_validators import validate_book


class BooksFrame(ttk.Frame):
    FIELDS = [
        ("Title", "title"), ("Author", "author"),
        ("Category", "category"), ("ISBN", "isbn"),
        ("Total Copies", "total_copies"), ("Available Copies", "available_copies"),
    ]

    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self.vars = {key: tk.StringVar() for _, key in self.FIELDS}
        self.search_var = tk.StringVar()
        self.selected_id = None
        self._build_ui()
        self.load_books()

    # ---------- UI ----------
    def _build_ui(self):
        # Search / filter bar
        bar = ttk.LabelFrame(self, text="Search (title, author or category)", padding=8)
        bar.pack(fill="x")
        entry = ttk.Entry(bar, textvariable=self.search_var, width=40)
        entry.pack(side="left", padx=5)
        entry.bind("<Return>", lambda e: self.load_books())
        ttk.Button(bar, text="Search", command=self.load_books).pack(side="left", padx=3)
        ttk.Button(bar, text="Show All", command=self.show_all).pack(side="left", padx=3)

        # Form
        form = ttk.LabelFrame(self, text="Book Details", padding=10)
        form.pack(fill="x", pady=8)
        for i, (label, key) in enumerate(self.FIELDS):
            r, c = divmod(i, 2)
            ttk.Label(form, text=label).grid(row=r, column=c * 2, sticky="w", padx=5, pady=4)
            ttk.Entry(form, textvariable=self.vars[key], width=32).grid(
                row=r, column=c * 2 + 1, padx=5, pady=4)

        # Buttons
        btns = ttk.Frame(self)
        btns.pack(fill="x")
        ttk.Button(btns, text="Add Book", command=self.add_book).pack(side="left", padx=4)
        ttk.Button(btns, text="Update Book", command=self.update_book).pack(side="left", padx=4)
        ttk.Button(btns, text="Delete Book", command=self.delete_book).pack(side="left", padx=4)
        ttk.Button(btns, text="Clear", command=self.clear_form).pack(side="left", padx=4)

        # Table
        cols = ("id", "title", "author", "category", "isbn", "total", "available")
        heads = ("ID", "Title", "Author", "Category", "ISBN", "Total", "Available")
        widths = (50, 230, 150, 110, 120, 60, 70)
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=10)
        for col, head, w in zip(cols, heads, widths):
            self.tree.heading(col, text=head)
            self.tree.column(col, width=w, anchor="w")
        self.tree.pack(fill="both", expand=True, pady=8)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        scroll = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")

    # ---------- DB helper ----------
    def _run(self, sql, params=(), fetch=False):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, params)
            if fetch:
                return cur.fetchall()
            conn.commit()
        finally:
            conn.close()

    def _form_data(self):
        return {key: var.get() for key, var in self.vars.items()}

    # ---------- Actions ----------
    def load_books(self):
        term = self.search_var.get().strip()
        try:
            if term:
                like = f"%{term}%"
                rows = self._run(
                    "SELECT book_id, title, author, category, isbn, total_copies, available_copies "
                    "FROM Books WHERE title LIKE %s OR author LIKE %s OR category LIKE %s "
                    "ORDER BY title", (like, like, like), fetch=True)
            else:
                rows = self._run(
                    "SELECT book_id, title, author, category, isbn, total_copies, available_copies "
                    "FROM Books ORDER BY title", fetch=True)
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
            return

        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", "end", values=row)

    def show_all(self):
        self.search_var.set("")
        self.load_books()

    def add_book(self):
        data = self._form_data()
        errors = validate_book(data)
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return
        try:
            self._run(
                "INSERT INTO Books (title, author, category, isbn, total_copies, available_copies) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (data["title"].strip(), data["author"].strip(), data["category"].strip(),
                 data["isbn"].strip(), int(data["total_copies"]), int(data["available_copies"])))
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "A book with this ISBN already exists.")
            return
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
            return
        messagebox.showinfo("Success", "Book added successfully.")
        self.clear_form()
        self.load_books()

    def update_book(self):
        if self.selected_id is None:
            messagebox.showwarning("No Selection", "Select a book from the table first.")
            return
        data = self._form_data()
        errors = validate_book(data)
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return
        try:
            self._run(
                "UPDATE Books SET title=%s, author=%s, category=%s, isbn=%s, "
                "total_copies=%s, available_copies=%s WHERE book_id=%s",
                (data["title"].strip(), data["author"].strip(), data["category"].strip(),
                 data["isbn"].strip(), int(data["total_copies"]),
                 int(data["available_copies"]), self.selected_id))
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Another book already uses this ISBN.")
            return
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
            return
        messagebox.showinfo("Success", "Book updated successfully.")
        self.clear_form()
        self.load_books()

    def delete_book(self):
        if self.selected_id is None:
            messagebox.showwarning("No Selection", "Select a book from the table first.")
            return
        try:
            # borrow_records uses ON DELETE CASCADE, so check first to avoid wiping history
            count = self._run("SELECT COUNT(*) FROM Borrow_Records WHERE book_id=%s",
                              (self.selected_id,), fetch=True)[0][0]
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
            return
        if count > 0:
            messagebox.showerror(
                "Cannot Delete", f"This book has {count} borrow record(s), so it cannot be deleted.")
            return
        if not messagebox.askyesno("Confirm Delete", "Delete the selected book?"):
            return
        try:
            self._run("DELETE FROM Books WHERE book_id=%s", (self.selected_id,))
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
            return
        messagebox.showinfo("Success", "Book deleted.")
        self.clear_form()
        self.load_books()

    def on_select(self, _event=None):
        sel = self.tree.selection()
        if not sel:
            return
        book_id, title, author, category, isbn, total, avail = self.tree.item(sel[0])["values"]
        self.selected_id = book_id
        for key, value in zip(
                ("title", "author", "category", "isbn", "total_copies", "available_copies"),
                (title, author, category, isbn, total, avail)):
            self.vars[key].set(value)

    def clear_form(self):
        self.selected_id = None
        for var in self.vars.values():
            var.set("")
        self.tree.selection_remove(self.tree.selection())