"""
visualization.py - PART B (Task 6)
Matplotlib charts: the required bar chart of student marks, plus
two extra charts (grade distribution and department averages).
Charts are saved as PNG images in the output/ folder.
"""
import os

import matplotlib
import matplotlib.pyplot as plt

from config import OUTPUT_DIR, PASS_MARKS
from analysis import department_summary

PASS_COLOR = "#2E86AB"
FAIL_COLOR = "#E4572E"


def _finish(fig, filename, show):
    path = os.path.join(OUTPUT_DIR, filename)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    if show and matplotlib.get_backend().lower() != "agg":
        plt.show()
    plt.close(fig)
    return path


def bar_chart_marks(df, show=True, filename="marks_bar_chart.png"):
    """REQUIRED: bar chart of student marks (blue = pass, red = fail)."""
    data = df.sort_values("marks", ascending=False)
    colors = [PASS_COLOR if m >= PASS_MARKS else FAIL_COLOR for m in data["marks"]]

    fig, ax = plt.subplots(figsize=(11, 6))
    bars = ax.bar(data["name"], data["marks"], color=colors, edgecolor="black", linewidth=0.5)

    # Show the marks value on top of every bar
    for bar, m in zip(bars, data["marks"]):
        ax.text(bar.get_x() + bar.get_width() / 2, m + 1, f"{m:.0f}",
                ha="center", va="bottom", fontsize=9)

    avg = data["marks"].mean()
    ax.axhline(avg, color="green", linestyle="--", label=f"Class average ({avg:.1f})")
    ax.axhline(PASS_MARKS, color="gray", linestyle=":", label=f"Pass marks ({PASS_MARKS})")

    ax.set_title("Student Marks Comparison", fontsize=15, fontweight="bold")
    ax.set_xlabel("Student Name", fontsize=12)
    ax.set_ylabel("Marks (out of 100)", fontsize=12)
    ax.set_ylim(0, 110)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    ax.legend(loc="upper right")
    ax.grid(axis="y", alpha=0.3)
    return _finish(fig, filename, show)


def grade_distribution_chart(df, show=True, filename="grade_distribution.png"):
    """EXTRA: pie chart showing how many students got each grade."""
    order = ["A+", "A", "B", "C", "D", "F"]
    counts = df["grade"].value_counts().reindex(order).dropna()
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(counts, labels=counts.index, autopct="%1.1f%%", startangle=90,
           colors=plt.cm.Set2.colors[:len(counts)], wedgeprops={"edgecolor": "white"})
    ax.set_title("Grade Distribution", fontsize=15, fontweight="bold")
    return _finish(fig, filename, show)


def department_average_chart(df, show=True, filename="department_average.png"):
    """EXTRA: average marks of each department."""
    summary = department_summary(df)
    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(summary["department"], summary["average"], color="#6A4C93", edgecolor="black")
    for bar, v in zip(bars, summary["average"]):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 1, f"{v:.1f}", ha="center")
    ax.set_title("Average Marks by Department", fontsize=14, fontweight="bold")
    ax.set_xlabel("Department")
    ax.set_ylabel("Average Marks")
    ax.set_ylim(0, 100)
    ax.grid(axis="y", alpha=0.3)
    return _finish(fig, filename, show)
