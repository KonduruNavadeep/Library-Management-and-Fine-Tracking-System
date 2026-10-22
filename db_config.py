# db_config.py - shared by every module
import mysql.connector

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""            # default: MySQL with no password
DB_NAME = "library_db"

# Personal override: if you have a MySQL password, put it in db_local.py
# (that file is never committed)
try:
    from db_local import DB_PASSWORD
except ImportError:
    pass


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )