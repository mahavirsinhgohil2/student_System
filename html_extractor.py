"""
html_extractor.py - Extract information from an HTML file
(required by the assignment description).

BeautifulSoup is used to read the HTML page and pull out:
  * the page title and headings
  * the student table  -> list of student dictionaries
  * all hyperlinks
The module can also GENERATE the HTML page from student records, so the
whole "write HTML -> read HTML" cycle can be demonstrated.
"""
from bs4 import BeautifulSoup

from config import HTML_FILE, FIELDS
from utils import clean_student, get_grade


def generate_html(students, path=HTML_FILE):
    """Create a simple HTML page that contains the student table."""
    rows = "\n".join(
        f"      <tr><td>{s['student_id']}</td><td>{s['name']}</td><td>{s['department']}</td>"
        f"<td>{s['semester']}</td><td>{s['marks']}</td></tr>"
        for s in students)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Student Result Sheet</title>
  <style>
    body  {{ font-family: Arial, sans-serif; margin: 30px; }}
    table {{ border-collapse: collapse; width: 80%; }}
    th, td {{ border: 1px solid #444; padding: 8px; text-align: left; }}
    th    {{ background: #2E86AB; color: white; }}
  </style>
</head>
<body>
  <h1>Aditya Silver Oak Institute of Technology</h1>
  <h2>Semester 5 - Result Sheet (2026-27)</h2>
  <p>Visit <a href="https://www.silveroakuni.ac.in">Silver Oak University</a> for more details.</p>
  <table id="students">
    <thead>
      <tr><th>Student ID</th><th>Name</th><th>Department</th><th>Semester</th><th>Marks</th></tr>
    </thead>
    <tbody>
{rows}
    </tbody>
  </table>
</body>
</html>
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


def extract_page_info(path=HTML_FILE):
    """Return title, headings and links found in the HTML file."""
    with open(path, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    return {
        "title": soup.title.get_text(strip=True) if soup.title else "",
        "headings": [h.get_text(strip=True) for h in soup.find_all(["h1", "h2", "h3"])],
        "links": [(a.get_text(strip=True), a.get("href")) for a in soup.find_all("a")],
    }


def extract_students(path=HTML_FILE):
    """Read the <table> in the HTML file and convert each row into a student dict."""
    with open(path, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    table = soup.find("table")
    if table is None:
        return []
    students = []
    for tr in table.find("tbody").find_all("tr") if table.find("tbody") else table.find_all("tr")[1:]:
        cells = [td.get_text(strip=True) for td in tr.find_all("td")]
        if len(cells) == len(FIELDS):
            students.append(clean_student(dict(zip(FIELDS, cells))))
    return students


def print_extracted_info(path=HTML_FILE):
    info = extract_page_info(path)
    students = extract_students(path)
    print("\n===== Information extracted from HTML file =====")
    print(f"Page title : {info['title']}")
    print("Headings   :")
    for h in info["headings"]:
        print(f"   - {h}")
    print("Links      :")
    for text, href in info["links"]:
        print(f"   - {text} -> {href}")
    print(f"Students found in table: {len(students)}")
    return students
