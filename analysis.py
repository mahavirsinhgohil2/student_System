"""
analysis.py - PART B (Task 4 & 5)
NumPy  : average, highest and lowest marks (plus extras).
Pandas : read, filter and sort student records.
"""
import numpy as np
import pandas as pd

from config import CSV_FILE, FIELDS, PASS_MARKS
from utils import get_grade, get_result


# ----------------------------------------------------------------------
# NumPy statistics (Task 4)
# ----------------------------------------------------------------------
def numpy_statistics(students):
    """Calculate statistics of marks using NumPy. Returns a dictionary."""
    if not students:
        return {}
    marks = np.array([s["marks"] for s in students], dtype=float)
    names = [s["name"] for s in students]

    stats = {
        "count": int(marks.size),
        "average": float(np.mean(marks)),
        "highest": float(np.max(marks)),
        "lowest": float(np.min(marks)),
        "median": float(np.median(marks)),
        "std_dev": float(np.std(marks)),
        "topper": names[int(np.argmax(marks))],
        "lowest_scorer": names[int(np.argmin(marks))],
        "pass_count": int(np.sum(marks >= PASS_MARKS)),
        "fail_count": int(np.sum(marks < PASS_MARKS)),
    }
    stats["pass_percentage"] = round(stats["pass_count"] / stats["count"] * 100, 2)
    return stats


def print_statistics(stats):
    if not stats:
        print("No data available for analysis.")
        return
    print("\n===== NumPy Marks Analysis =====")
    print(f"Total students    : {stats['count']}")
    print(f"Average marks     : {stats['average']:.2f}")
    print(f"Highest marks     : {stats['highest']:.2f}  ({stats['topper']})")
    print(f"Lowest marks      : {stats['lowest']:.2f}  ({stats['lowest_scorer']})")
    print(f"Median marks      : {stats['median']:.2f}")
    print(f"Standard deviation: {stats['std_dev']:.2f}")
    print(f"Passed / Failed   : {stats['pass_count']} / {stats['fail_count']} "
          f"({stats['pass_percentage']}% pass)")


# ----------------------------------------------------------------------
# Pandas operations (Task 5)
# ----------------------------------------------------------------------
def load_dataframe(path=CSV_FILE):
    """Read the CSV file into a Pandas DataFrame and add Grade / Result columns."""
    df = pd.read_csv(path)[FIELDS]
    return add_grade_columns(df)


def dataframe_from_records(students):
    """Build a DataFrame from a list of dictionaries (e.g. MySQL records)."""
    df = pd.DataFrame(students, columns=FIELDS)
    return add_grade_columns(df)


def add_grade_columns(df):
    df = df.copy()
    df["grade"] = df["marks"].apply(get_grade)
    df["result"] = df["marks"].apply(get_result)
    return df


def filter_students(df, department=None, min_marks=None, max_marks=None,
                    grade=None, result=None, name_contains=None):
    """Filter the DataFrame using any combination of conditions."""
    out = df
    if department:
        out = out[out["department"].str.upper() == department.upper()]
    if min_marks is not None:
        out = out[out["marks"] >= min_marks]
    if max_marks is not None:
        out = out[out["marks"] <= max_marks]
    if grade:
        out = out[out["grade"] == grade.upper()]
    if result:
        out = out[out["result"].str.lower() == result.lower()]
    if name_contains:
        out = out[out["name"].str.contains(name_contains, case=False, na=False)]
    return out


def sort_students(df, by="marks", ascending=False):
    """Sort the DataFrame by any column."""
    return df.sort_values(by=by, ascending=ascending).reset_index(drop=True)


def top_n(df, n=5):
    """Return the top-n students by marks (merit list with rank)."""
    ranked = sort_students(df, "marks", False).head(n).copy()
    ranked.insert(0, "rank", range(1, len(ranked) + 1))
    return ranked


def department_summary(df):
    """Group by department: student count, average, highest and lowest marks."""
    summary = df.groupby("department")["marks"].agg(
        students="count", average="mean", highest="max", lowest="min").round(2)
    return summary.reset_index()


def print_dataframe(df, title):
    print(f"\n{title}")
    if df.empty:
        print("  (no matching records)")
    else:
        print(df.to_string(index=False))
