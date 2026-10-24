"""
create_admin.py - run this to add a login user (the Users table starts empty).

    python3 create_admin.py

Run it once for an Admin and once more for a test Librarian.
The password is stored as a bcrypt hash, never as plain text.
"""

import getpass

import bcrypt
import mysql.connector

from db_config import get_connection


def main():
    username = input("Username: ").strip()
    password = getpass.getpass("Password (hidden while typing): ")
    role = input("Role (Admin or Librarian) [Admin]: ").strip() or "Admin"

    if not username or not password:
        print("Username and password cannot be empty.")
        return
    if role not in ("Admin", "Librarian"):
        print("Role must be Admin or Librarian.")
        return
    if len(password.encode()) > 72:
        print("Password is too long (72 characters at most).")
        return

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Users (username, password, role) VALUES (%s, %s, %s)",
            (username, hashed, role),
        )
        conn.commit()
        print(f"User '{username}' created as {role}.")
    except mysql.connector.Error as e:
        print("Could not create the user:", e.msg)
    finally:
        if conn is not None and conn.is_connected():
            conn.close()


if __name__ == "__main__":
    main()
