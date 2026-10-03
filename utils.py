"""
utils.py - Helper functions shared by all modules:
validation, grade calculation and pretty table printing.
"""
from config import VALID_DEPARTMENTS, PASS_MARKS


def get_grade(marks):
    """Convert marks (0-100) into a letter grade."""
    if marks >= 90:
        return "A+"
    if marks >= 80:
        return "A"
    if marks >= 70:
        return "B"
    if marks >= 60:
        return "C"
    if marks >= PASS_MARKS:
        return "D"
    return "F"


def get_result(marks):
    """Return 'Pass' or 'Fail' using the pass mark from config."""
    return "Pass" if marks >= PASS_MARKS else "Fail"


def validate_student(student):
    """
    Validate one student dictionary.
    Returns (True, "") if valid, otherwise (False, "reason").
    """
    try:
        if int(student["student_id"]) <= 0:
            return False, "Student ID must be a positive number."
    except (ValueError, TypeError, KeyError):
        return False, "Student ID must be a number."

    if not str(student.get("name", "")).strip():
        return False, "Name cannot be empty."

    if str(student.get("department", "")).upper() not in VALID_DEPARTMENTS:
        return False, f"Department must be one of {VALID_DEPARTMENTS}."

    try:
        if not 1 <= int(student["semester"]) <= 8:
            return False, "Semester must be between 1 and 8."
    except (ValueError, TypeError, KeyError):
        return False, "Semester must be a number."

    try:
        if not 0 <= float(student["marks"]) <= 100:
            return False, "Marks must be between 0 and 100."
    except (ValueError, TypeError, KeyError):
        return False, "Marks must be a number."

    return True, ""


def clean_student(student):
    """Return a student dict with correct data types and tidy text."""
    return {
        "student_id": int(student["student_id"]),
        "name": str(student["name"]).strip().title(),
        "department": str(student["department"]).strip().upper(),
        "semester": int(student["semester"]),
        "marks": round(float(student["marks"]), 2),
    }


def print_table(students, title="Student Records"):
    """Print a list of student dictionaries as a neat text table."""
    print(f"\n{title}")
    if not students:
        print("  (no records found)")
        return
    line = "+" + "-" * 12 + "+" + "-" * 24 + "+" + "-" * 12 + "+" + "-" * 10 + "+" + "-" * 9 + "+" + "-" * 7 + "+"
    print(line)
    print(f"| {'Student ID':<10} | {'Name':<22} | {'Department':<10} | {'Semester':<8} | {'Marks':<7} | {'Grade':<5} |")
    print(line)
    for s in students:
        print(f"| {s['student_id']:<10} | {s['name']:<22} | {s['department']:<10} | "
              f"{s['semester']:<8} | {float(s['marks']):<7.1f} | {get_grade(float(s['marks'])):<5} |")
    print(line)
    print(f"Total records: {len(students)}")
