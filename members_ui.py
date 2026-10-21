"""members_ui.py - Member Management screen: Register, View, Update, Delete + Search (Member 2)."""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import mysql.connector

from db_config import get_connection      # written by Member 1
from inventory_validators import validate_member


class MembersFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.type_var = tk.StringVar(value="Student")
        self.date_var = tk.StringVar(value=date.today().isoformat())
        self.search_var = tk.StringVar()
        self.selected_id = None
        self._build_ui()
        self.load_members()

    # ---------- UI ----------
    def _build_ui(self):
        bar = ttk.LabelFrame(self, text="Search (name, email or phone)", padding=8)
        bar.pack(fill="x")
        entry = ttk.Entry(bar, textvariable=self.search_var, width=40)
        entry.pack(side="left", padx=5)
        entry.bind("<Return>", lambda e: self.load_members())
        ttk.Button(bar, text="Search", command=self.load_members).pack(side="left", padx=3)
        ttk.Button(bar, text="Show All", command=self.show_all).pack(side="left", padx=3)

        form = ttk.LabelFrame(self, text="Member Details", padding=10)
        form.pack(fill="x", pady=8)

        def row(r, c, label, widget):
            ttk.Label(form, text=label).grid(row=r, column=c * 2, sticky="w", padx=5, pady=4)
            widget.grid(row=r, column=c * 2 + 1, padx=5, pady=4)

        row(0, 0, "Name", ttk.Entry(form, textvariable=self.name_var, width=32))
        row(0, 1, "Email", ttk.Entry(form, textvariable=self.email_var, width=32))
        row(1, 0, "Phone (10 digits)", ttk.Entry(form, textvariable=self.phone_var, width=32))
        row(1, 1, "Member Type", ttk.Combobox(
            form, textvariable=self.type_var, values=("Student", "Faculty"),
            state="readonly", width=29))
        row(2, 0, "Join Date (YYYY-MM-DD)", ttk.Entry(form, textvariable=self.date_var, width=32))

        btns = ttk.Frame(self)
        btns.pack(fill="x")
        ttk.Button(btns, text="Register Member", command=self.add_member).pack(side="left", padx=4)
        ttk.Button(btns, text="Update Member", command=self.update_member).pack(side="left", padx=4)
        ttk.Button(btns, text="Delete Member", command=self.delete_member).pack(side="left", padx=4)
        ttk.Button(btns, text="Clear", command=self.clear_form).pack(side="left", padx=4)

        cols = ("id", "name", "email", "phone", "type", "joined")
        heads = ("ID", "Name", "Email", "Phone", "Type", "Joined")
        widths = (50, 180, 230, 110, 80, 100)
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
        return {
            "name": self.name_var.get(), "email": self.email_var.get(),
            "phone": self.phone_var.get(), "member_type": self.type_var.get(),
            "join_date": self.date_var.get(),
        }

    # ---------- Actions ----------
    def load_members(self):
        term = self.search_var.get().strip()
        base = "SELECT member_id, name, email, phone, member_type, join_date FROM Members"
        try:
            if term:
                like = f"%{term}%"
                rows = self._run(base + " WHERE name LIKE %s OR email LIKE %s OR phone LIKE %s "
                                 "ORDER BY name", (like, like, like), fetch=True)
            else:
                rows = self._run(base + " ORDER BY name", fetch=True)
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
            return

        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", "end", values=row)

    def show_all(self):
        self.search_var.set("")
        self.load_members()

    def add_member(self):
        d = self._form_data()
        errors = validate_member(d)
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return
        try:
            self._run(
                "INSERT INTO Members (name, email, phone, member_type, join_date) "
                "VALUES (%s, %s, %s, %s, %s)",
                (d["name"].strip(), d["email"].strip(), d["phone"].strip(),
                 d["member_type"], d["join_date"].strip()))
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "A member with this email already exists.")
            return
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
            return
        messagebox.showinfo("Success", "Member registered successfully.")
        self.clear_form()
        self.load_members()

    def update_member(self):
        if self.selected_id is None:
            messagebox.showwarning("No Selection", "Select a member from the table first.")
            return
        d = self._form_data()
        errors = validate_member(d)
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return
        try:
            self._run(
                "UPDATE Members SET name=%s, email=%s, phone=%s, member_type=%s, join_date=%s "
                "WHERE member_id=%s",
                (d["name"].strip(), d["email"].strip(), d["phone"].strip(),
                 d["member_type"], d["join_date"].strip(), self.selected_id))
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Another member already uses this email.")
            return
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
            return
        messagebox.showinfo("Success", "Member updated successfully.")
        self.clear_form()
        self.load_members()

    def delete_member(self):
        if self.selected_id is None:
            messagebox.showwarning("No Selection", "Select a member from the table first.")
            return
        if not messagebox.askyesno("Confirm Delete", "Delete the selected member?"):
            return
        try:
            self._run("DELETE FROM Members WHERE member_id=%s", (self.selected_id,))
        except mysql.connector.IntegrityError:
            messagebox.showerror(
                "Cannot Delete", "This member has borrow records, so cannot be deleted.")
            return
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
            return
        messagebox.showinfo("Success", "Member deleted.")
        self.clear_form()
        self.load_members()

    def on_select(self, _event=None):
        sel = self.tree.selection()
        if not sel:
            return
        mid, name, email, phone, mtype, joined = self.tree.item(sel[0])["values"]
        self.selected_id = mid
        self.name_var.set(name)
        self.email_var.set(email)
        # Treeview turns "0987654321" into an int and drops the leading zero
        self.phone_var.set(str(phone).zfill(10))
        self.type_var.set(mtype)
        self.date_var.set(joined)

    def clear_form(self):
        self.selected_id = None
        self.name_var.set("")
        self.email_var.set("")
        self.phone_var.set("")
        self.type_var.set("Student")
        self.date_var.set(date.today().isoformat())
        self.tree.selection_remove(self.tree.selection())