"""inventory_validators.py - input validation for Book and Member forms (Member 2).
Field lengths match the library_db schema (books and members tables)."""
import re

EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.]+$")
PHONE_RE = re.compile(r"^\d{10}$")            # exactly 10 digits
REGNO_RE = re.compile(r"^[A-Za-z0-9]+$")      # letters and digits only


def _is_int(value):
    try:
        int(value)
        return True
    except (ValueError, TypeError):
        return False


def validate_book(d):
    """d: dict of strings - title, author, category, isbn, total_copies, available_copies.
    Returns a list of error messages (empty list = valid)."""
    errors = []
    limits = {"title": 150, "author": 100, "category": 50, "isbn": 20}
    for field, max_len in limits.items():
        value = d[field].strip()
        if not value:
            errors.append(f"{field.capitalize()} cannot be empty.")
        elif len(value) > max_len:
            errors.append(f"{field.capitalize()} cannot be longer than {max_len} characters.")

    if not _is_int(d["total_copies"]) or int(d["total_copies"]) < 0:
        errors.append("Total copies must be a whole number (0 or more).")
    if not _is_int(d["available_copies"]) or int(d["available_copies"]) < 0:
        errors.append("Available copies must be a whole number (0 or more).")

    if not errors and int(d["available_copies"]) > int(d["total_copies"]):
        errors.append("Available copies cannot exceed total copies.")
    return errors


def validate_member(d):
    """d: dict of strings - register_no, full_name, department, email, phone."""
    errors = []

    reg = d["register_no"].strip()
    if not reg:
        errors.append("Register number cannot be empty.")
    elif not REGNO_RE.match(reg):
        errors.append("Register number can contain only letters and digits.")
    elif len(reg) > 20:
        errors.append("Register number cannot be longer than 20 characters.")

    for field, label, max_len in (("full_name", "Full name", 100), ("department", "Department", 50)):
        value = d[field].strip()
        if not value:
            errors.append(f"{label} cannot be empty.")
        elif len(value) > max_len:
            errors.append(f"{label} cannot be longer than {max_len} characters.")

    email = d["email"].strip()
    if not email:
        errors.append("Email cannot be empty.")
    elif not EMAIL_RE.match(email):
        errors.append("Enter a valid email address (e.g. name@example.com).")
    elif len(email) > 100:
        errors.append("Email cannot be longer than 100 characters.")

    phone = d["phone"].strip()
    if not phone:
        errors.append("Phone cannot be empty.")
    elif not PHONE_RE.match(phone):
        errors.append("Phone must be exactly 10 digits.")
    return errors