"""validators.py - input validation for Book and Member forms (Member 2)."""
import re
from datetime import datetime, date

EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.]+$")
PHONE_RE = re.compile(r"^\d{10}$")          # exactly 10 digits
# For Indian mobile numbers only, use: r"^[6-9]\d{9}$"


def _is_int(value):
    try:
        int(value)
        return True
    except (ValueError, TypeError):
        return False


def validate_book(d):
    """d is a dict of strings: title, author, category, isbn,
    total_copies, available_copies. Returns a list of error messages."""
    errors = []
    for field in ("title", "author", "category", "isbn"):
        if not d[field].strip():
            errors.append(f"{field.capitalize()} cannot be empty.")

    if not _is_int(d["total_copies"]) or int(d["total_copies"]) < 0:
        errors.append("Total copies must be a whole number (0 or more).")
    if not _is_int(d["available_copies"]) or int(d["available_copies"]) < 0:
        errors.append("Available copies must be a whole number (0 or more).")

    if not errors and int(d["available_copies"]) > int(d["total_copies"]):
        errors.append("Available copies cannot exceed total copies.")
    return errors


def validate_member(d):
    """d is a dict of strings: name, email, phone, member_type, join_date."""
    errors = []
    if not d["name"].strip():
        errors.append("Name cannot be empty.")

    if not d["email"].strip():
        errors.append("Email cannot be empty.")
    elif not EMAIL_RE.match(d["email"].strip()):
        errors.append("Enter a valid email address (e.g. name@example.com).")

    if not d["phone"].strip():
        errors.append("Phone cannot be empty.")
    elif not PHONE_RE.match(d["phone"].strip()):
        errors.append("Phone must be exactly 10 digits.")

    if d["member_type"] not in ("Student", "Faculty"):
        errors.append("Select a member type (Student or Faculty).")

    if not d["join_date"].strip():
        errors.append("Join date cannot be empty.")
    else:
        try:
            joined = datetime.strptime(d["join_date"].strip(), "%Y-%m-%d").date()
            if joined > date.today():
                errors.append("Join date cannot be in the future.")
        except ValueError:
            errors.append("Join date must be a valid date in YYYY-MM-DD format.")
    return errors