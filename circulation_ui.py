"""
Module: circulation_ui.py
Role: Member 3 - Circulation & Fine Logic Lead (Connected to MySQL)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import mysql.connector
from validators import is_positive_integer, validate_issue_and_due_dates

# Configure your MySQL root password here
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "6872",  
    "database": "library_db"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


class CirculationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management - Circulation & Fines (Member 3)")
        self.root.geometry("900x620")
        self.root.resizable(False, False)

        header = tk.Frame(self.root, bg="#2C3E50", height=50)
        header.pack(fill="x")
        tk.Label(
            header,
            text="Circulation & Fine Management Module",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#2C3E50"
        ).pack(pady=12)

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=15, pady=15)

        self.issue_tab = ttk.Frame(notebook)
        self.return_tab = ttk.Frame(notebook)
        self.fine_tab = ttk.Frame(notebook)

        notebook.add(self.issue_tab, text=" Issue Book ")
        notebook.add(self.return_tab, text=" Return Book ")
        notebook.add(self.fine_tab, text=" Fine Tracking & Payment ")

        self.setup_issue_tab()
        self.setup_return_tab()
        self.setup_fine_tab()

    # 1. ISSUE BOOK SCREEN (Calls Stored Procedure IssueBook)
    def setup_issue_tab(self):
        container = tk.LabelFrame(
            self.issue_tab,
            text=" Issue a Book to Member ",
            font=("Arial", 11, "bold"),
            padx=25,
            pady=25
        )
        container.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(container, text="Member ID (Numeric):", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=10)
        self.issue_member_entry = tk.Entry(container, font=("Arial", 10), width=30)
        self.issue_member_entry.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(container, text="Book ID (Numeric):", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=10)
        self.issue_book_entry = tk.Entry(container, font=("Arial", 10), width=30)
        self.issue_book_entry.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(container, text="Issue Date (YYYY-MM-DD):", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", pady=10)
        self.issue_date_entry = tk.Entry(container, font=("Arial", 10), width=30)
        self.issue_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.issue_date_entry.grid(row=2, column=1, pady=10, padx=10)

        tk.Label(container, text="Due Date (YYYY-MM-DD):", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", pady=10)
        self.due_date_entry = tk.Entry(container, font=("Arial", 10), width=30)
        self.due_date_entry.insert(0, (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"))
        self.due_date_entry.grid(row=3, column=1, pady=10, padx=10)

        tk.Button(
            container,
            text="Confirm & Issue Book",
            font=("Arial", 11, "bold"),
            bg="#27AE60",
            fg="white",
            padx=10,
            pady=5,
            command=self.handle_issue_book
        ).grid(row=4, column=1, sticky="w", pady=25)

    def handle_issue_book(self):
        member_id = self.issue_member_entry.get().strip()
        book_id = self.issue_book_entry.get().strip()
        issue_date = self.issue_date_entry.get().strip()
        due_date = self.due_date_entry.get().strip()

        valid_m, err_m = is_positive_integer(member_id, "Member ID")
        if not valid_m:
            messagebox.showwarning("Validation Error", err_m)
            return

        valid_b, err_b = is_positive_integer(book_id, "Book ID")
        if not valid_b:
            messagebox.showwarning("Validation Error", err_b)
            return

        valid_dates, date_msg = validate_issue_and_due_dates(issue_date, due_date)
        if not valid_dates:
            messagebox.showerror("Date Validation Error", date_msg)
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.callproc("IssueBook", (int(book_id), int(member_id), issue_date, due_date))
            conn.commit()
            cursor.close()
            conn.close()

            self.refresh_return_table()
            messagebox.showinfo("Success", f"Book #{book_id} issued to Member #{member_id} via Stored Procedure!")
            self.issue_member_entry.delete(0, tk.END)
            self.issue_book_entry.delete(0, tk.END)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    # 2. RETURN BOOK SCREEN (Fires AutoCalculateFineOnReturn Trigger)
    def setup_return_tab(self):
        frame = tk.Frame(self.return_tab, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        top_bar = tk.Frame(frame)
        top_bar.pack(fill="x", pady=5)
        tk.Label(top_bar, text="Active Issued Books", font=("Arial", 11, "bold")).pack(side="left")
        tk.Label(top_bar, text="Return Date (YYYY-MM-DD):", font=("Arial", 10)).pack(side="left", padx=(30, 5))
        self.return_date_entry = tk.Entry(top_bar, font=("Arial", 10), width=15)
        self.return_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.return_date_entry.pack(side="left")

        cols = ("issue_id", "book_id", "title", "member_id", "issue_date", "due_date", "status")
        self.return_tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)
        headings = ["Issue ID", "Book ID", "Book Title", "Member ID", "Issue Date", "Due Date", "Status"]
        widths = [70, 70, 220, 90, 100, 100, 90]
        for col, text, w in zip(cols, headings, widths):
            self.return_tree.heading(col, text=text)
            self.return_tree.column(col, width=w, anchor="center" if col != "title" else "w")
        self.return_tree.pack(fill="both", expand=True, pady=5)

        btn_bar = tk.Frame(frame)
        btn_bar.pack(fill="x", pady=10)
        tk.Button(
            btn_bar,
            text="Return Selected Book",
            font=("Arial", 10, "bold"),
            bg="#2980B9",
            fg="white",
            padx=12,
            pady=5,
            command=self.handle_return_book
        ).pack(side="left")
        tk.Button(
            btn_bar,
            text="Refresh Table",
            font=("Arial", 10),
            padx=10,
            pady=5,
            command=self.refresh_return_table
        ).pack(side="left", padx=10)

        self.refresh_return_table()

    def refresh_return_table(self):
        for item in self.return_tree.get_children():
            self.return_tree.delete(item)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
                SELECT br.issue_id, br.book_id, b.title, br.member_id, br.issue_date, br.due_date, br.status
                FROM Borrow_Records br
                JOIN Books b ON br.book_id = b.book_id
                WHERE br.status = 'Issued'
                ORDER BY br.issue_id DESC
            """
            cursor.execute(query)
            for row in cursor.fetchall():
                self.return_tree.insert("", "end", values=row)
            cursor.close()
            conn.close()
        except mysql.connector.Error:
            pass

    def handle_return_book(self):
        selected = self.return_tree.selection()
        if not selected:
            messagebox.showwarning("Select Item", "Please select an issued book record to return.")
            return

        values = self.return_tree.item(selected)["values"]
        issue_id, book_id = values[0], values[1]
        return_date = self.return_date_entry.get().strip()

        try:
            conn = get_connection()
            cursor = conn.cursor()
            # Updating Borrow_Records fires AutoCalculateFineOnReturn Trigger if return_date > due_date
            cursor.execute("""
                UPDATE Borrow_Records
                SET return_date = %s, status = 'Returned'
                WHERE issue_id = %s
            """, (return_date, issue_id))

            cursor.execute("""
                UPDATE Books
                SET available_copies = available_copies + 1
                WHERE book_id = %s
            """, (book_id,))

            conn.commit()
            cursor.close()
            conn.close()

            self.refresh_return_table()
            self.refresh_fines_table()
            messagebox.showinfo(
                "Return Logged",
                f"Issue #{issue_id} returned on {return_date}.\nIf overdue, the SQL Trigger automatically generated a fine."
            )
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    # 3. FINE PAYMENT SCREEN
    def setup_fine_tab(self):
        frame = tk.Frame(self.fine_tab, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Overdue Fines Tracking", font=("Arial", 11, "bold")).pack(anchor="w", pady=5)

        cols = ("fine_id", "issue_id", "member_id", "fine_amount", "payment_status", "payment_date")
        self.fine_tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)
        headings = ["Fine ID", "Issue ID", "Member ID", "Fine Amount (Rs)", "Status", "Payment Date"]
        for col, text in zip(cols, headings):
            self.fine_tree.heading(col, text=text)
            self.fine_tree.column(col, anchor="center", width=130)
        self.fine_tree.pack(fill="both", expand=True, pady=5)

        btn_bar = tk.Frame(frame)
        btn_bar.pack(fill="x", pady=10)
        tk.Button(
            btn_bar,
            text="Mark Selected Fine as Paid",
            font=("Arial", 10, "bold"),
            bg="#D35400",
            fg="white",
            padx=12,
            pady=5,
            command=self.handle_pay_fine
        ).pack(side="left")
        tk.Button(
            btn_bar,
            text="Refresh Fines",
            font=("Arial", 10),
            padx=10,
            pady=5,
            command=self.refresh_fines_table
        ).pack(side="left", padx=10)

        self.refresh_fines_table()

    def refresh_fines_table(self):
        for item in self.fine_tree.get_children():
            self.fine_tree.delete(item)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
                SELECT f.fine_id, f.issue_id, br.member_id, f.fine_amount, f.payment_status, IFNULL(f.payment_date, '-')
                FROM Fines f
                JOIN Borrow_Records br ON f.issue_id = br.issue_id
                ORDER BY f.fine_id DESC
            """
            cursor.execute(query)
            for row in cursor.fetchall():
                self.fine_tree.insert("", "end", values=row)
            cursor.close()
            conn.close()
        except mysql.connector.Error:
            pass
    def handle_pay_fine(self):
        selected = self.fine_tree.selection()
        if not selected:
            messagebox.showwarning("Select Fine", "Please select a fine entry from the table.")
            return

        values = self.fine_tree.item(selected)["values"]
        fine_id, status = values[0], values[4]

        if status == "Paid":
            messagebox.showinfo("Already Paid", f"Fine #{fine_id} is already marked as Paid.")
            return

        today_str = datetime.now().strftime("%Y-%m-%d")
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Fines
                SET payment_status = 'Paid', payment_date = %s
                WHERE fine_id = %s
            """, (today_str, fine_id))
            conn.commit()
            cursor.close()
            conn.close()

            self.refresh_fines_table()
            messagebox.showinfo("Payment Recorded", f"Fine #{fine_id} updated to 'Paid' on {today_str}.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))


if __name__ == "__main__":
    root_window = tk.Tk()
    app = CirculationApp(root_window)
    root_window.mainloop()     