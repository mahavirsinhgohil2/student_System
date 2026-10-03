-- schema.sql : MySQL database structure for the Student Information & Visualization System
-- (The Python program creates these automatically, this file is for reference / manual setup.)

CREATE DATABASE IF NOT EXISTS student_db;
USE student_db;

CREATE TABLE IF NOT EXISTS students (
    student_id INT PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    department VARCHAR(20)  NOT NULL,
    semester   TINYINT      NOT NULL,
    marks      DECIMAL(5,2) NOT NULL
);

-- Sample CRUD queries used by database.py
-- INSERT INTO students VALUES (116, 'Demo Student', 'IT', 5, 70);
-- SELECT * FROM students ORDER BY student_id;
-- UPDATE students SET marks = 90 WHERE student_id = 116;
-- DELETE FROM students WHERE student_id = 116;
