import tkinter as tk
from login import LoginWindow
from dashboard import Dashboard, PAGE_BUILDERS

# Import all individual module frames
from books_ui import BooksFrame
from members_ui import MembersFrame
from circulation_ui import CirculationFrame
from app import LibraryDashboardApp

class ReportsLauncher(tk.Frame):
    """Adapter frame to launch the standalone Reports window from within the Dashboard content area."""
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Analytics & Reports", font=("Helvetica", 16, "bold")).pack(pady=30)
        tk.Button(
            self, 
            text="Open Reports Dashboard", 
            font=("Helvetica", 12),
            bg="#2563eb",
            fg="white",
            command=self.launch_reports
        ).pack(pady=10)

    def launch_reports(self):
        reports_window = LibraryDashboardApp()
        reports_window.mainloop()

def main():
    while True:
        # 1. Launch the Login Window
        login_app = LoginWindow()
        login_app.mainloop()

        # 2. Exit if the window was closed without a successful login
        if not login_app.user:
            break 

        # 3. Register the UI frames to the Dashboard's navigation menu
        PAGE_BUILDERS["Books"] = BooksFrame
        PAGE_BUILDERS["Members"] = MembersFrame
        PAGE_BUILDERS["Issue / Return"] = CirculationFrame
        PAGE_BUILDERS["Fines"] = CirculationFrame  # Maps to the same frame containing the Fines tab
        PAGE_BUILDERS["Reports"] = ReportsLauncher

        # 4. Launch the Main Dashboard with user credentials
        user = login_app.user
        dashboard_app = Dashboard(username=user["username"], role=user["role"])
        dashboard_app.mainloop()

        # 5. Restart the loop if the user clicked Logout, otherwise exit completely
        if getattr(dashboard_app, 'logged_out', False) == False:
            break

if __name__ == "__main__":
    main()