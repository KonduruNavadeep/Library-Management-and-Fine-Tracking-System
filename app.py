import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "251132",
    "password": "123456",  # <-- Replace with your MySQL password
    "database": "library_db"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

class LibraryDashboardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Analytics & Reports Dashboard")
        self.geometry("1100x720")
        self.configure(bg="#f1f5f9")

        # Configure TTK Styles
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        
        # Table Styling
        self.style.configure("Treeview", 
                             background="#ffffff", 
                             foreground="#1e293b", 
                             rowheight=26, 
                             fieldbackground="#ffffff",
                             font=("Segoe UI", 10))
        self.style.configure("Treeview.Heading", 
                             background="#0f172a", 
                             foreground="#ffffff", 
                             font=("Segoe UI", 10, "bold"))
        self.style.map("Treeview", background=[("selected", "#cbd5e1")])

        # Header Title
        header_frame = tk.Frame(self, bg="#0f172a", padx=20, pady=15)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="📚 Library Analytics & Reports Dashboard", 
                 font=("Segoe UI", 18, "bold"), fg="#ffffff", bg="#0f172a").pack(anchor="w")
        tk.Label(header_frame, text="Circulation KPIs, Revenue Summaries, and Live Overdue Defaulters Roster", 
                 font=("Segoe UI", 10), fg="#94a3b8", bg="#0f172a").pack(anchor="w")

        # KPI Metrics Cards Frame
        self.kpi_frame = tk.Frame(self, bg="#f1f5f9", padx=15, pady=10)
        self.kpi_frame.pack(fill="x")

        # Create Metric Cards
        self.lbl_collected = self._create_card(self.kpi_frame, "TOTAL FINES COLLECTED", "₹0.00", "#16a34a", 0)
        self.lbl_pending = self._create_card(self.kpi_frame, "TOTAL PENDING DUES", "₹0.00", "#dc2626", 1)
        self.lbl_defaulters = self._create_card(self.kpi_frame, "ACTIVE DEFAULTERS", "0 Records", "#d97706", 2)

        # Tabbed Layout for Data Tables
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=10)

        # Tab 1: Overdue Defaulters View
        self.tab_defaulters = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_defaulters, text=" 🚨 Overdue Defaulters (Live View) ")
        self._build_defaulters_tab()

        # Tab 2: Department-Wise Breakdown
        self.tab_departments = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_departments, text=" 🏢 Department-Wise Dues ")
        self._build_departments_tab()

        # Tab 3: Top 5 Defaulters Ranking
        self.tab_top_defaulters = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_top_defaulters, text=" 🏆 Top Defaulters ")
        self._build_top_defaulters_tab()

        # Tab 4: Book Category Analysis
        self.tab_categories = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_categories, text=" 📖 Category Circulation ")
        self._build_categories_tab()

        # Refresh Button & Footer
        footer_frame = tk.Frame(self, bg="#f1f5f9", padx=15, pady=5)
        footer_frame.pack(fill="x")
        
        btn_refresh = tk.Button(footer_frame, text="🔄 Refresh All Data", font=("Segoe UI", 10, "bold"),
                                bg="#2563eb", fg="#ffffff", padx=12, pady=6, relief="flat", command=self.load_all_data)
        btn_refresh.pack(side="right")

        # Initial Load
        self.load_all_data()

    def _create_card(self, parent, title, default_val, text_color, col_idx):
        card = tk.Frame(parent, bg="#ffffff", bd=1, relief="solid", padx=15, pady=12)
        card.grid(row=0, column=col_idx, padx=8, pady=5, sticky="nsew")
        parent.grid_columnconfigure(col_idx, weight=1)

        tk.Label(card, text=title, font=("Segoe UI", 9, "bold"), fg="#64748b", bg="#ffffff").pack(anchor="w")
        val_label = tk.Label(card, text=default_val, font=("Segoe UI", 18, "bold"), fg=text_color, bg="#ffffff")
        val_label.pack(anchor="w", pady=(5, 0))
        return val_label

    def _create_treeview(self, parent, columns, col_widths):
        container = ttk.Frame(parent)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        tree = ttk.Treeview(container, columns=columns, show="headings", selectmode="browse")
        vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(container, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        tree.pack(fill="both", expand=True)

        for col, width in zip(columns, col_widths):
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor="center" if col in ["Reg No", "Dept", "Days Late", "Status", "Total Unpaid Books"] else "w")
        return tree

    def _build_defaulters_tab(self):
        # Filter controls
        filter_frame = tk.Frame(self.tab_defaulters, bg="#f8fafc", padx=10, pady=8)
        filter_frame.pack(fill="x")

        tk.Label(filter_frame, text="Filter by Department: ", font=("Segoe UI", 10, "bold"), bg="#f8fafc").pack(side="left")
        self.dept_filter_var = tk.StringVar(value="All")
        self.dept_combobox = ttk.Combobox(filter_frame, textvariable=self.dept_filter_var, state="readonly", width=15)
        self.dept_combobox.pack(side="left", padx=5)
        self.dept_combobox.bind("<<ComboboxSelected>>", lambda e: self.filter_defaulters())

        cols = ("Reg No", "Member Name", "Dept", "Phone", "Book Title", "Due Date", "Days Late", "Fine Amount", "Status")
        widths = [90, 150, 70, 110, 220, 100, 80, 100, 90]
        self.tree_defaulters = self._create_treeview(self.tab_defaulters, cols, widths)

    def _build_departments_tab(self):
        cols = ("Department", "Defaulters Count", "Fines Issued", "Collected Amount", "Pending Dues")
        widths = [140, 130, 120, 140, 140]
        self.tree_departments = self._create_treeview(self.tab_departments, cols, widths)

    def _build_top_defaulters_tab(self):
        cols = ("Reg No", "Member Name", "Department", "Phone", "Total Unpaid Books", "Pending Fine Debt")
        widths = [100, 180, 100, 120, 140, 140]
        self.tree_top_defaulters = self._create_treeview(self.tab_top_defaulters, cols, widths)

    def _build_categories_tab(self):
        cols = ("Category", "Borrow Count", "Overdue Incidents", "Total Fines Generated")
        widths = [160, 140, 140, 160]
        self.tree_categories = self._create_treeview(self.tab_categories, cols, widths)

    def load_all_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            # 1. Update Metric Cards
            cursor.execute("""
                SELECT 
                    COALESCE(SUM(CASE WHEN payment_status = 'Paid' THEN fine_amount ELSE 0 END), 0) AS collected,
                    COALESCE(SUM(CASE WHEN payment_status = 'Unpaid' THEN fine_amount ELSE 0 END), 0) AS pending,
                    COUNT(CASE WHEN payment_status = 'Unpaid' THEN 1 END) AS pending_count
                FROM Fines;
            """)
            stats = cursor.fetchone()
            self.lbl_collected.config(text=f"₹{stats['collected']:,.2f}")
            self.lbl_pending.config(text=f"₹{stats['pending']:,.2f}")
            self.lbl_defaulters.config(text=f"{stats['pending_count']} Records")

            # 2. Load Defaulters View
            cursor.execute("""
                SELECT register_no, member_name, department, phone, book_title, due_date, days_overdue, fine_amount, payment_status
                FROM Overdue_Defaulters_View;
            """)
            self.raw_defaulters_data = cursor.fetchall()
            
            # Populate filter combobox
            depts = sorted(list({r["department"] for r in self.raw_defaulters_data if r["department"]}))
            self.dept_combobox["values"] = ["All"] + depts
            self.filter_defaulters()

            # 3. Department Breakdown
            self.tree_departments.delete(*self.tree_departments.get_children())
            cursor.execute("""
                SELECT 
                    m.department,
                    COUNT(DISTINCT m.member_id) AS total_defaulters,
                    COUNT(f.fine_id) AS total_fines_issued,
                    COALESCE(SUM(CASE WHEN f.payment_status = 'Paid' THEN f.fine_amount ELSE 0 END), 0) AS fines_collected,
                    COALESCE(SUM(CASE WHEN payment_status = 'Unpaid' THEN f.fine_amount ELSE 0 END), 0) AS fines_pending
                FROM Members m
                JOIN Borrow_Records br ON m.member_id = br.member_id
                JOIN Fines f ON br.issue_id = f.issue_id
                GROUP BY m.department
                ORDER BY fines_pending DESC;
            """)
            for row in cursor.fetchall():
                self.tree_departments.insert("", "end", values=(
                    row["department"], row["total_defaulters"], row["total_fines_issued"],
                    f"₹{float(row['fines_collected']):,.2f}", f"₹{float(row['fines_pending']):,.2f}"
                ))

            # 4. Top Defaulters
            self.tree_top_defaulters.delete(*self.tree_top_defaulters.get_children())
            cursor.execute("""
                SELECT 
                    m.register_no,
                    m.full_name AS member_name,
                    m.department,
                    m.phone,
                    COUNT(f.fine_id) AS unpaid_books_count,
                    SUM(f.fine_amount) AS total_pending_debt
                FROM Members m
                JOIN Borrow_Records br ON m.member_id = br.member_id
                JOIN Fines f ON br.issue_id = f.issue_id
                WHERE f.payment_status = 'Unpaid'
                GROUP BY m.member_id, m.register_no, m.full_name, m.department, m.phone
                ORDER BY total_pending_debt DESC
                LIMIT 5;
            """)
            for row in cursor.fetchall():
                self.tree_top_defaulters.insert("", "end", values=(
                    row["register_no"], row["member_name"], row["department"], row["phone"],
                    row["unpaid_books_count"], f"₹{float(row['total_pending_debt']):,.2f}"
                ))

            # 5. Book Categories
            self.tree_categories.delete(*self.tree_categories.get_children())
            cursor.execute("""
                SELECT 
                    b.category,
                    COUNT(br.issue_id) AS times_borrowed,
                    COUNT(f.fine_id) AS overdue_instances,
                    COALESCE(SUM(f.fine_amount), 0.00) AS total_fines_generated
                FROM Books b
                LEFT JOIN Borrow_Records br ON b.book_id = br.book_id
                LEFT JOIN Fines f ON br.issue_id = f.issue_id
                GROUP BY b.category
                ORDER BY times_borrowed DESC;
            """)
            for row in cursor.fetchall():
                self.tree_categories.insert("", "end", values=(
                    row["category"], row["times_borrowed"], row["overdue_instances"],
                    f"₹{float(row['total_fines_generated']):,.2f}"
                ))

            cursor.close()
            conn.close()

        except Exception as e:
            messagebox.showerror("Database Connection Error", f"Failed to retrieve data:\n{str(e)}")

    def filter_defaulters(self):
        self.tree_defaulters.delete(*self.tree_defaulters.get_children())
        selected = self.dept_filter_var.get()

        for r in self.raw_defaulters_data:
            if selected == "All" or r["department"] == selected:
                self.tree_defaulters.insert("", "end", values=(
                    r["register_no"],
                    r["member_name"],
                    r["department"],
                    r["phone"],
                    r["book_title"],
                    str(r["due_date"]),
                    f"{r['days_overdue']} days",
                    f"₹{float(r['fine_amount']):.2f}",
                    r["payment_status"]
                ))

if __name__ == "__main__":
    app = LibraryDashboardApp()
    app.mainloop()