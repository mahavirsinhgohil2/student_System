"""
file_handler.py - PART A (Task 1 & 3)
Store student records in a CSV file, and read / display them.
Also provides add / update / delete on the CSV so the file stays usable
on its own (without MySQL).
"""
import csv
import os

from config import CSV_FILE, FIELDS
from utils import validate_student, clean_student, print_table


def read_students(path=CSV_FILE):
    """Read all records from the CSV file and return a list of dictionaries."""
    if not os.path.exists(path):
        return []
    students = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            students.append(clean_student(row))
    return students


def write_students(students, path=CSV_FILE):
    """Overwrite the CSV file with the given list of student dictionaries."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        for s in students:
            writer.writerow({k: s[k] for k in FIELDS})


def add_student(student, path=CSV_FILE):
    """Append one new student. Returns (success, message)."""
    ok, msg = validate_student(student)
    if not ok:
        return False, msg
    student = clean_student(student)
    students = read_students(path)
    if any(s["student_id"] == student["student_id"] for s in students):
        return False, f"Student ID {student['student_id']} already exists."
    students.append(student)
    write_students(students, path)
    return True, "Student added to CSV file."


def update_student(student_id, updates, path=CSV_FILE):
    """Update fields of an existing student. Returns (success, message)."""
    students = read_students(path)
    for s in students:
        if s["student_id"] == int(student_id):
            merged = {**s, **updates}
            ok, msg = validate_student(merged)
            if not ok:
                return False, msg
            s.update(clean_student(merged))
            write_students(students, path)
            return True, "CSV record updated."
    return False, f"Student ID {student_id} not found."


def delete_student(student_id, path=CSV_FILE):
    """Delete a student by ID. Returns (success, message)."""
    students = read_students(path)
    remaining = [s for s in students if s["student_id"] != int(student_id)]
    if len(remaining) == len(students):
        return False, f"Student ID {student_id} not found."
    write_students(remaining, path)
    return True, "CSV record deleted."


def display_students(path=CSV_FILE):
    """Read the CSV file and print the records in a table."""
    print_table(read_students(path), "Student Records (from CSV file)")
