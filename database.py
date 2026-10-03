"""
database.py - PART A (Task 2 & 3)
CRUD operations on a MySQL database using mysql-connector-python.
All queries use parameters (%s) to prevent SQL injection.
"""
import mysql.connector
from mysql.connector import Error

from config import DB_CONFIG, DB_NAME, TABLE_NAME
from utils import validate_student, clean_student, print_table


class StudentDB:
    """Wrapper class around the MySQL connection."""

    def __init__(self):
        self.conn = None

    # ------------------------------------------------------------------
    # Connection + setup
    # ------------------------------------------------------------------
    def connect(self):
        """Connect to MySQL, create the database and table if missing."""
        try:
            self.conn = mysql.connector.connect(**DB_CONFIG)
            cur = self.conn.cursor()
            cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            cur.execute(f"USE {DB_NAME}")
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    student_id INT PRIMARY KEY,
                    name       VARCHAR(100) NOT NULL,
                    department VARCHAR(20)  NOT NULL,
                    semester   TINYINT      NOT NULL,
                    marks      DECIMAL(5,2) NOT NULL
                )""")
            self.conn.commit()
            cur.close()
            return True
        except Error as e:
            print(f"[MySQL ERROR] Could not connect: {e}")
            self.conn = None
            return False

    def close(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()

    def _run(self, sql, params=None, fetch=False):
        """Execute one query safely. Returns rows (fetch) or affected row count."""
        cur = self.conn.cursor(dictionary=True)
        try:
            cur.execute(sql, params or ())
            if fetch:
                return cur.fetchall()
            self.conn.commit()
            return cur.rowcount
        finally:
            cur.close()

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------
    def create(self, student):
        ok, msg = validate_student(student)
        if not ok:
            return False, msg
        s = clean_student(student)
        try:
            self._run(f"INSERT INTO {TABLE_NAME} VALUES (%s,%s,%s,%s,%s)",
                      (s["student_id"], s["name"], s["department"], s["semester"], s["marks"]))
            return True, "Student inserted into MySQL."
        except Error as e:
            if e.errno == 1062:  # duplicate primary key
                return False, f"Student ID {s['student_id']} already exists."
            return False, f"MySQL error: {e}"

    # ------------------------------------------------------------------
    # READ
    # ------------------------------------------------------------------
    def read_all(self):
        rows = self._run(f"SELECT * FROM {TABLE_NAME} ORDER BY student_id", fetch=True)
        return [self._to_python(r) for r in rows]

    def read_one(self, student_id):
        rows = self._run(f"SELECT * FROM {TABLE_NAME} WHERE student_id=%s", (student_id,), fetch=True)
        return self._to_python(rows[0]) if rows else None

    def search_by_name(self, text):
        rows = self._run(f"SELECT * FROM {TABLE_NAME} WHERE name LIKE %s ORDER BY name",
                         (f"%{text}%",), fetch=True)
        return [self._to_python(r) for r in rows]

    def display(self):
        print_table(self.read_all(), "Student Records (from MySQL)")

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------
    def update(self, student_id, updates):
        current = self.read_one(student_id)
        if not current:
            return False, f"Student ID {student_id} not found."
        merged = {**current, **updates}
        ok, msg = validate_student(merged)
        if not ok:
            return False, msg
        s = clean_student(merged)
        self._run(f"UPDATE {TABLE_NAME} SET name=%s, department=%s, semester=%s, marks=%s "
                  f"WHERE student_id=%s",
                  (s["name"], s["department"], s["semester"], s["marks"], s["student_id"]))
        return True, "MySQL record updated."

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------
    def delete(self, student_id):
        count = self._run(f"DELETE FROM {TABLE_NAME} WHERE student_id=%s", (student_id,))
        if count:
            return True, "MySQL record deleted."
        return False, f"Student ID {student_id} not found."

    # ------------------------------------------------------------------
    # Integration helpers (CSV <-> MySQL)
    # ------------------------------------------------------------------
    def import_students(self, students):
        """Insert/replace many students (used for CSV -> MySQL sync)."""
        count = 0
        for st in students:
            s = clean_student(st)
            self._run(f"REPLACE INTO {TABLE_NAME} VALUES (%s,%s,%s,%s,%s)",
                      (s["student_id"], s["name"], s["department"], s["semester"], s["marks"]))
            count += 1
        return count

    @staticmethod
    def _to_python(row):
        """MySQL returns DECIMAL as Decimal - convert to normal float/int."""
        return {"student_id": int(row["student_id"]), "name": row["name"],
                "department": row["department"], "semester": int(row["semester"]),
                "marks": float(row["marks"])}
