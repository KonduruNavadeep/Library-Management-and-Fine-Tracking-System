"""members_ui.py - Member Management screen: Register, View, Update, Delete + Search (Member 2).
Works with the members table: member_id, register_no, full_name, department, email, phone."""
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

from db_config import get_connection      # shared connection file
from inventory_validators import validate_member


class MembersFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self.reg_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.dept_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.search_var = tk.StringVar()
        self.selected_id = None
        self._build_ui()
        self.load_members()

    # ---------- UI ----------
    def _build_ui(self):
        bar = ttk.LabelFrame(self, text="Search (name, register no, email, department or phone)", padding=8)
        bar.pack(fill="x")
        entry = ttk.Entry(bar, textvariable=self.search_var, width=40)
        entry.pack(side="left", padx=5)
        entry.bind("<Return>", lambda e: self.load_members())
        ttk.Button(bar, text="Search", command=self.load_members).pack(side="left", padx=3)
        ttk.Button(bar, text="Show All", command=self.show_all).pack(side="left", padx=3)

        form = ttk.LabelFrame(self, text="Member Details", padding=10)
        form.pack(fill="x", pady=8)

        fields = [
            ("Register No", self.reg_var), ("Full Name", self.name_var),
            ("Department", self.dept_var), ("Email", self.email_var),
            ("Phone (10 digits)", self.phone_var),
        ]
        for i, (label, var) in enumerate(fields):
            r, c = divmod(i, 2)
            ttk.Label(form, text=label).grid(row=r, column=c * 2, sticky="w", padx=5, pady=4)
            ttk.Entry(form, textvariable=var, width=32).grid(row=r, column=c * 2 + 1, padx=5, pady=4)

        btns = ttk.Frame(self)
        btns.pack(fill="x")
        ttk.Button(btns, text="Register Member", command=self.add_member).pack(side="left", padx=4)
        ttk.Button(btns, text="Update Member", command=self.update_member).pack(side="left", padx=4)
        ttk.Button(btns, text="Delete Member", command=self.delete_member).pack(side="left", padx=4)
        ttk.Button(btns, text="Clear", command=self.clear_form).pack(side="left", padx=4)

        cols = ("id", "reg", "name", "dept", "email", "phone")
        heads = ("ID", "Register No", "Full Name", "Department", "Email", "Phone")
        widths = (45, 90, 160, 90, 210, 110)
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
            "register_no": self.reg_var.get(), "full_name": self.name_var.get(),
            "department": self.dept_var.get(), "email": self.email_var.get(),
            "phone": self.phone_var.get(),
        }

    def _params(self, d):
        return (d["register_no"].strip(), d["full_name"].strip(), d["department"].strip(),
                d["email"].strip(), d["phone"].strip())

    # ---------- Actions ----------
    def load_members(self):
        term = self.search_var.get().strip()
        base = "SELECT member_id, register_no, full_name, department, email, phone FROM Members"
        try:
            if term:
                like = f"%{term}%"
                rows = self._run(
                    base + " WHERE full_name LIKE %s OR register_no LIKE %s OR email LIKE %s "
                           "OR department LIKE %s OR phone LIKE %s ORDER BY member_id",
                    (like, like, like, like, like), fetch=True)
            else:
                rows = self._run(base + " ORDER BY member_id", fetch=True)
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
            self._run("INSERT INTO Members (register_no, full_name, department, email, phone) "
                      "VALUES (%s, %s, %s, %s, %s)", self._params(d))
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "A member with this register number or email already exists.")
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
            self._run("UPDATE Members SET register_no=%s, full_name=%s, department=%s, "
                      "email=%s, phone=%s WHERE member_id=%s", self._params(d) + (self.selected_id,))
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Another member already uses this register number or email.")
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
        try:
            # borrow_records uses ON DELETE CASCADE, so check first to avoid wiping history
            count = self._run("SELECT COUNT(*) FROM Borrow_Records WHERE member_id=%s",
                              (self.selected_id,), fetch=True)[0][0]
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
            return
        if count > 0:
            messagebox.showerror("Cannot Delete",
                                 f"This member has {count} borrow record(s), so cannot be deleted.")
            return
        if not messagebox.askyesno("Confirm Delete", "Delete the selected member?"):
            return
        try:
            self._run("DELETE FROM Members WHERE member_id=%s", (self.selected_id,))
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
        mid, reg, name, dept, email, phone = self.tree.item(sel[0])["values"]
        self.selected_id = mid
        self.reg_var.set(reg)
        self.name_var.set(name)
        self.dept_var.set(dept)
        self.email_var.set(email)
        self.phone_var.set(str(phone).zfill(10))   # Treeview drops a leading zero

    def clear_form(self):
        self.selected_id = None
        for var in (self.reg_var, self.name_var, self.dept_var, self.email_var, self.phone_var):
            var.set("")
        self.tree.selection_remove(self.tree.selection())
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Member Management")
    root.geometry("950x650")

    app = MembersFrame(root)
    app.pack(fill="both", expand=True)

    root.mainloop()