"""
Run this script ONCE after importing schema.sql to set proper password hashes.
Usage: python seed_passwords.py
"""
import sys
from werkzeug.security import generate_password_hash

# Generate hashes to paste into MySQL, or update directly if DB is configured
credentials = [
    ("superadmin@skilltrack.com", "SuperAdmin@123"),
    ("admin@skilltrack.com",      "Admin@123"),
    ("trainer@skilltrack.com",    "Trainer@123"),
    ("student@skilltrack.com",    "Student@123"),
    ("marketer@skilltrack.com",   "Marketer@123"),
]

print("-- Run these SQL statements after importing schema.sql\n")
for email, pw in credentials:
    hashed = generate_password_hash(pw)
    print(f"UPDATE users SET password_hash='{hashed}' WHERE email='{email}';")

print("\n-- Done. These passwords will work for login:")
for email, pw in credentials:
    print(f"{email} : {pw}")
