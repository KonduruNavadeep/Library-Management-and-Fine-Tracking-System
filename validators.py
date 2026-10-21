"""
Module: validators.py
Purpose: Input validation helper functions for forms (Dates, IDs, and Empty Checks)
"""

from datetime import datetime
import re

def is_not_empty(value):
    """
    Checks if a field is not empty or just whitespace[cite: 2].
    Returns (True, '') if valid, otherwise (False, 'Error message').
    """
    if value is None or str(value).strip() == "":
        return False, "This field cannot be empty."
    return True, ""


def is_valid_date_format(date_str):
    #Validates that a date is in the format YYYY-MM-DD[cite: 2].
    if not date_str or not str(date_str).strip():
        return False, "Date cannot be empty."
    
    try:
        parsed_date = datetime.strptime(str(date_str).strip(), "%Y-%m-%d").date()
        return True, parsed_date
    except ValueError:
        return False, "Invalid date format. Expected format: YYYY-MM-DD (e.g., 2026-10-25)."


def validate_issue_and_due_dates(issue_date_str, due_date_str):
    """
    Validates that both dates are valid and that due_date is strictly after issue_date[cite: 2].
    """
    valid_issue, res_issue = is_valid_date_format(issue_date_str)
    if not valid_issue:
        return False, f"Issue Date Error: {res_issue}"
    
    valid_due, res_due = is_valid_date_format(due_date_str)
    if not valid_due:
        return False, f"Due Date Error: {res_due}"
    
    if res_due <= res_issue:
        return False, "Due date must be after the issue date."
        
    return True, "Dates are valid."


def is_positive_integer(value, field_name="Value"):
    #Validates that an ID or quantity is a positive whole number[cite: 2].
    valid, msg = is_not_empty(value)
    if not valid:
        return False, f"{field_name} cannot be empty."
        
    try:
        num = int(str(value).strip())
        if num <= 0:
            return False, f"{field_name} must be greater than zero."
        return True, ""
    except ValueError:
        return False, f"{field_name} must be a valid positive integer."


def is_valid_fine_amount(value):
    #Validates that fine payment amount is a non-negative decimal or integer[cite: 2].
    valid, msg = is_not_empty(value)
    if not valid:
        return False, "Fine amount cannot be empty."
        
    try:
        amt = float(str(value).strip())
        if amt < 0:
            return False, "Fine amount cannot be negative."
        return True, ""
    except ValueError:
        return False, "Fine amount must be a valid number."


#  Local Test Block 
if __name__ == "__main__":
    print("Testing Validation Functions...\n")
    
    # 1. Test Empty Field
    print("Empty Check ('   '):", is_not_empty("   "))
    print("Empty Check ('CS3106'):", is_not_empty("CS3106"))
    
    # 2. Test Issue & Due Dates
    print("\nDate Check (2026-10-21, 2026-10-28):", validate_issue_and_due_dates("2026-10-21", "2026-10-28"))
    print("Date Check (Due earlier than Issue):", validate_issue_and_due_dates("2026-10-25", "2026-10-20"))
    print("Date Check (Invalid format):", validate_issue_and_due_dates("21/10/2026", "2026-10-28"))

    # 3. Test Numeric IDs and Fines
    print("\nPositive Int Check ('105'):", is_positive_integer("105", "Book ID"))
    print("Positive Int Check ('-5'):", is_positive_integer("-5", "Book ID"))
    print("Fine Check ('25.50'):", is_valid_fine_amount("25.50"))
    print("Fine Check ('-10'):", is_valid_fine_amount("-10"))