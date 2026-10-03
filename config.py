"""
config.py - Central configuration for the Student Information & Visualization System.
Database credentials can be overridden with environment variables so that
no password is hard-coded in the source when the project is shared.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

CSV_FILE = os.path.join(DATA_DIR, "students.csv")
HTML_FILE = os.path.join(DATA_DIR, "students.html")

# Order of columns used everywhere (CSV header, MySQL table, DataFrame)
FIELDS = ["student_id", "name", "department", "semester", "marks"]

VALID_DEPARTMENTS = ["CE", "CSE", "IT", "CSE-CS"]
PASS_MARKS = 40

# ---- MySQL settings (override with environment variables if needed) ----
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
}
DB_NAME = os.getenv("DB_NAME", "student_db")
TABLE_NAME = "students"

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
