from http.server import SimpleHTTPRequestHandler, HTTPServer
import mysql.connector
import json
import webbrowser

DB_CONFIG = {
    "host": "localhost",
    "user": "251132",
    "password": "123456",  # <-- Replace with your MySQL password
    "database": "library_db"
}

def fetch_data():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    
    # 1. Summary Metrics
    cursor.execute("""
        SELECT 
            COALESCE(SUM(CASE WHEN payment_status = 'Paid' THEN fine_amount ELSE 0 END), 0) AS collected,
            COALESCE(SUM(CASE WHEN payment_status = 'Unpaid' THEN fine_amount ELSE 0 END), 0) AS pending,
            COUNT(CASE WHEN payment_status = 'Unpaid' THEN 1 END) AS pending_count
        FROM Fines;
    """)
    stats = cursor.fetchone()

    # 2. Defaulters View Data
    cursor.execute("""
        SELECT register_no, member_name, department, phone, book_title, due_date, days_overdue, fine_amount, payment_status
        FROM Overdue_Defaulters_View;
    """)
    defaulters = cursor.fetchall()

    # 3. Department Breakdown
    cursor.execute("""
        SELECT m.department, COALESCE(SUM(f.fine_amount), 0) AS debt
        FROM Members m
        JOIN Borrow_Records br ON m.member_id = br.member_id
        JOIN Fines f ON br.issue_id = f.issue_id
        WHERE f.payment_status = 'Unpaid'
        GROUP BY m.department;
    """)
    depts = cursor.fetchall()

    cursor.close()
    conn.close()
    
    # Convert dates to string for JSON serialization
    for row in defaulters:
        if row.get('due_date'):
            row['due_date'] = str(row['due_date'])
        row['fine_amount'] = float(row['fine_amount'])
    for d in depts:
        d['debt'] = float(d['debt'])

    return stats, defaulters, depts

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Library Fine Analytics Dashboard</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 30px; background: #f8fafc; color: #1e293b; }
        h1 { margin-bottom: 5px; }
        .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 25px 0; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; }
        .card h3 { margin: 0; font-size: 14px; color: #64748b; text-transform: uppercase; }
        .card .val { font-size: 28px; font-weight: bold; margin-top: 10px; color: #0f172a; }
        table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #e2e8f0; font-size: 14px; }
        th { background: #0f172a; color: white; }
        tr:hover { background: #f1f5f9; }
        .badge { background: #fee2e2; color: #b91c1c; padding: 4px 8px; border-radius: 4px; font-weight: 600; font-size: 12px; }
    </style>
</head>
<body>
    <h1>📚 Library Analytics & Defaulters Dashboard</h1>
    <p>Live circulation & late fee monitoring powered by <code>Overdue_Defaulters_View</code></p>
    
    <div class="grid">
        <div class="card"><h3>Total Fines Collected</h3><div class="val" style="color: #16a34a;">₹__COLLECTED__</div></div>
        <div class="card"><h3>Total Pending Dues</h3><div class="val" style="color: #dc2626;">₹__PENDING__</div></div>
        <div class="card"><h3>Active Defaulters</h3><div class="val">__COUNT__ Records</div></div>
    </div>

    <h2>🚨 Current Defaulters List</h2>
    <table>
        <thead>
            <tr>
                <th>Reg No</th><th>Member Name</th><th>Department</th><th>Phone</th>
                <th>Book Title</th><th>Due Date</th><th>Days Late</th><th>Fine Amount</th><th>Status</th>
            </tr>
        </thead>
        <tbody>
            __ROWS__
        </tbody>
    </table>
</body>
</html>
"""

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            stats, defaulters, _ = fetch_data()
            rows_html = "".join([
                f"<tr><td>{r['register_no']}</td><td><b>{r['member_name']}</b></td><td>{r['department']}</td><td>{r['phone']}</td>"
                f"<td>{r['book_title']}</td><td>{r['due_date']}</td><td>{r['days_overdue']} days</td>"
                f"<td>₹{r['fine_amount']:.2f}</td><td><span class='badge'>{r['payment_status']}</span></td></tr>"
                for r in defaulters
            ])
            html = HTML_TEMPLATE.replace("__COLLECTED__", f"{float(stats['collected']):,.2f}")
            html = html.replace("__PENDING__", f"{float(stats['pending']):,.2f}")
            html = html.replace("__COUNT__", str(stats['pending_count']))
            html = html.replace("__ROWS__", rows_html)

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

print("Server starting at http://localhost:8000 ...")
webbrowser.open("http://localhost:8000")
HTTPServer(("localhost", 8000), Handler).serve_forever()