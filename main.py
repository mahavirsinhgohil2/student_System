"""
main.py - Student Information & Visualization System
Fundamentals of Python Programming (2010042318) - Innovative Assignment

Run:
    python main.py            -> interactive menu
    python main.py --demo     -> runs every feature automatically (good for a quick demo)
"""
import sys

from flask import Flask, jsonify

import file_handler as fh
import analysis as an
import visualization as viz
import html_extractor as hx
from config import CSV_FILE, HTML_FILE
from database import StudentDB
from utils import print_table


# ----------------------------------------------------------------------
# Small input helpers
# ----------------------------------------------------------------------
def ask(prompt, default=None):
    value = input(prompt).strip()
    return value if value else default


def ask_student(existing=None):
    """Ask for student details. When 'existing' is given, Enter keeps the old value."""
    def field(label, key):
        if existing:
            return ask(f"{label} [{existing[key]}]: ", str(existing[key]))
        return input(f"{label}: ").strip()
    student = {}
    student["student_id"] = existing["student_id"] if existing else input("Student ID: ").strip()
    student["name"] = field("Name", "name")
    student["department"] = field("Department (CE/CSE/IT/CSE-CS)", "department")
    student["semester"] = field("Semester", "semester")
    student["marks"] = field("Marks (0-100)", "marks")
    return student


def report(result):
    ok, msg = result
    print(("[OK] " if ok else "[!] ") + msg)


# ----------------------------------------------------------------------
# Menus
# ----------------------------------------------------------------------
def csv_menu():
    while True:
        print("\n--- CSV FILE MENU ---")
        print("1. Display records\n2. Add student\n3. Update student\n4. Delete student\n0. Back")
        c = input("Choice: ").strip()
        if c == "1":
            fh.display_students()
        elif c == "2":
            report(fh.add_student(ask_student()))
        elif c == "3":
            sid = input("Student ID to update: ").strip()
            old = next((s for s in fh.read_students() if str(s["student_id"]) == sid), None)
            if old:
                new = ask_student(old)
                report(fh.update_student(sid, new))
            else:
                print("[!] Student not found.")
        elif c == "4":
            report(fh.delete_student(input("Student ID to delete: ").strip()))
        elif c == "0":
            return


def mysql_menu(db):
    while True:
        print("\n--- MySQL CRUD MENU ---")
        print("1. Create (insert)\n2. Read all\n3. Search by name\n4. Update\n5. Delete\n"
              "6. Import CSV -> MySQL\n7. Export MySQL -> CSV\n0. Back")
        c = input("Choice: ").strip()
        if c == "1":
            report(db.create(ask_student()))
        elif c == "2":
            db.display()
        elif c == "3":
            print_table(db.search_by_name(input("Name contains: ").strip()), "Search results")
        elif c == "4":
            sid = input("Student ID to update: ").strip()
            old = db.read_one(sid) if sid.isdigit() else None
            if old:
                report(db.update(sid, ask_student(old)))
            else:
                print("[!] Student not found.")
        elif c == "5":
            sid = input("Student ID to delete: ").strip()
            report(db.delete(sid))
        elif c == "6":
            print(f"[OK] {db.import_students(fh.read_students())} records imported from CSV.")
        elif c == "7":
            fh.write_students(db.read_all())
            print("[OK] MySQL data written to CSV file.")
        elif c == "0":
            return


def analysis_menu():
    df = an.load_dataframe()
    while True:
        print("\n--- DATA ANALYSIS MENU ---")
        print("1. NumPy statistics (average / highest / lowest)\n2. Filter records (Pandas)\n"
              "3. Sort records (Pandas)\n4. Top 5 merit list\n5. Department summary\n0. Back")
        c = input("Choice: ").strip()
        if c == "1":
            an.print_statistics(an.numpy_statistics(fh.read_students()))
        elif c == "2":
            dept = ask("Department (Enter to skip): ")
            mn = ask("Minimum marks (Enter to skip): ")
            res = ask("Result Pass/Fail (Enter to skip): ")
            out = an.filter_students(df, department=dept,
                                     min_marks=float(mn) if mn else None, result=res)
            an.print_dataframe(out, "Filtered records")
        elif c == "3":
            col = ask("Sort by column [marks]: ", "marks")
            order = ask("Ascending? (y/n) [n]: ", "n").lower() == "y"
            if col in df.columns:
                an.print_dataframe(an.sort_students(df, col, order), f"Sorted by {col}")
            else:
                print("[!] Invalid column.")
        elif c == "4":
            an.print_dataframe(an.top_n(df, 5), "Top 5 students")
        elif c == "5":
            an.print_dataframe(an.department_summary(df), "Department-wise summary")
        elif c == "0":
            return


def chart_menu():
    df = an.load_dataframe()
    print("\n--- CHARTS MENU ---")
    print("1. Bar chart of marks\n2. Grade distribution (pie)\n3. Department average\n4. All charts\n0. Back")
    c = input("Choice: ").strip()
    paths = []
    if c in ("1", "4"):
        paths.append(viz.bar_chart_marks(df))
    if c in ("2", "4"):
        paths.append(viz.grade_distribution_chart(df))
    if c in ("3", "4"):
        paths.append(viz.department_average_chart(df))
    for p in paths:
        print(f"[OK] Chart saved: {p}")


def html_menu():
    print("\n--- HTML MENU ---")
    print("1. Generate HTML result sheet from CSV\n2. Extract information from HTML file\n"
          "3. Import students from HTML -> CSV\n0. Back")
    c = input("Choice: ").strip()
    if c == "1":
        print(f"[OK] HTML created: {hx.generate_html(fh.read_students())}")
    elif c == "2":
        students = hx.print_extracted_info()
        print_table(students, "Students extracted from HTML table")
    elif c == "3":
        students = hx.extract_students()
        fh.write_students(students)
        print(f"[OK] {len(students)} students from HTML saved to {CSV_FILE}")


def main_menu():
    db = StudentDB()
    db_ready = db.connect()
    if not db_ready:
        print("MySQL is not available - MySQL menu will be disabled. "
              "Check DB_USER / DB_PASSWORD in config.py or environment variables.")
    while True:
        print("\n" + "=" * 50)
        print("  STUDENT INFORMATION & VISUALIZATION SYSTEM")
        print("=" * 50)
        print("1. CSV file operations\n2. MySQL CRUD operations\n3. Data analysis (NumPy & Pandas)\n"
              "4. Charts (Matplotlib)\n5. HTML extraction\n0. Exit")
        c = input("Choice: ").strip()
        if c == "1":
            csv_menu()
        elif c == "2":
            mysql_menu(db) if db_ready else print("[!] MySQL not connected.")
        elif c == "3":
            analysis_menu()
        elif c == "4":
            chart_menu()
        elif c == "5":
            html_menu()
        elif c == "0":
            db.close()
            print("Goodbye!")
            return


# ----------------------------------------------------------------------
# Non-interactive demo - runs every feature once
# ----------------------------------------------------------------------
def run_demo():
    print("#" * 60 + "\n PART A : FILE HANDLING & DATABASE\n" + "#" * 60)
    fh.display_students()

    print("\n-- CSV CRUD --")
    report(fh.add_student({"student_id": 116, "name": "demo student", "department": "it",
                           "semester": 5, "marks": 70}))
    report(fh.update_student(116, {"marks": 77}))
    report(fh.delete_student(116))

    db = StudentDB()
    if db.connect():
        print("\n-- MySQL CRUD --")
        print(f"[OK] {db.import_students(fh.read_students())} records imported CSV -> MySQL")
        db.display()
        report(db.create({"student_id": 116, "name": "demo student", "department": "IT",
                          "semester": 5, "marks": 70}))
        report(db.create({"student_id": 116, "name": "duplicate", "department": "IT",
                          "semester": 5, "marks": 70}))
        print("Read one :", db.read_one(116))
        report(db.update(116, {"marks": 90}))
        print("After update:", db.read_one(116))
        print_table(db.search_by_name("demo"), "Search 'demo'")
        report(db.delete(116))
        report(db.delete(116))
        db.close()
    else:
        print("MySQL demo skipped (server not reachable).")

    print("\n" + "#" * 60 + "\n PART B : DATA ANALYSIS\n" + "#" * 60)
    students = fh.read_students()
    an.print_statistics(an.numpy_statistics(students))
    df = an.load_dataframe()
    an.print_dataframe(an.filter_students(df, department="CSE", min_marks=50), "Filter: CSE students with marks >= 50")
    an.print_dataframe(an.filter_students(df, result="Fail"), "Filter: failed students")
    an.print_dataframe(an.sort_students(df, "marks", False).head(8), "Sorted by marks (descending) - first 8")
    an.print_dataframe(an.top_n(df, 5), "Top 5 merit list")
    an.print_dataframe(an.department_summary(df), "Department summary")

    print("\n-- Matplotlib charts --")
    for path in (viz.bar_chart_marks(df, show=False),
                 viz.grade_distribution_chart(df, show=False),
                 viz.department_average_chart(df, show=False)):
        print("[OK] saved", path)

    print("\n" + "#" * 60 + "\n HTML EXTRACTION\n" + "#" * 60)
    hx.generate_html(students)
    extracted = hx.print_extracted_info()
    print("Round-trip check (CSV == HTML data):", extracted == students)


app = Flask(__name__)


@app.get("/")
def index():
    """Return the CSV-backed student summary for the Vercel deployment."""
    students = fh.read_students()
    return jsonify({
        "name": "Student Information & Visualization System",
        "students": students,
        "statistics": an.numpy_statistics(students),
    })


if __name__ == "__main__":
    if "--demo" in sys.argv:
        run_demo()
    else:
        main_menu()
