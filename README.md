# Student Information & Visualization System
Fundamentals of Python Programming (2010042318) - Innovative Assignment
Aditya Silver Oak Institute of Technology | Semester 5 | 2026-27

A Python application to manage student records (CSV + MySQL), analyse marks
(NumPy, Pandas), draw charts (Matplotlib) and extract data from an HTML file (BeautifulSoup).

## Project structure
| File | Purpose |
|------|---------|
| `main.py` | Menu-driven program + `--demo` mode |
| `config.py` | File paths, MySQL settings, constants |
| `utils.py` | Validation, grade calculation, table printing |
| `file_handler.py` | CSV storage, read / display, add / update / delete |
| `database.py` | MySQL CRUD operations |
| `analysis.py` | NumPy statistics + Pandas filter / sort / group |
| `visualization.py` | Matplotlib bar chart (+ pie chart, department chart) |
| `html_extractor.py` | Generate and read an HTML page with BeautifulSoup |
| `schema.sql` | MySQL table definition |
| `data/students.csv` | Sample data (15 students) |

## Setup
1. Install Python 3.9+ and MySQL Server (or XAMPP / MySQL Workbench) and start the MySQL service.
2. Install libraries:
   ```
   pip install -r requirements.txt
   ```
3. Set your MySQL login (Windows CMD example - or edit `DB_CONFIG` in `config.py`):
   ```
   set DB_USER=root
   set DB_PASSWORD=your_password
   ```
   On Linux/Mac use `export DB_USER=root` and `export DB_PASSWORD=your_password`.
   The database `student_db` and the `students` table are created automatically.

## Run
```
python main.py          # interactive menu
python main.py --demo   # runs every feature automatically
```
Charts are saved in the `output/` folder.

## Features
* CSV storage with add / update / delete / display
* MySQL CRUD (parameterised queries), search by name, CSV <-> MySQL sync
* NumPy: average, highest, lowest, median, standard deviation, pass %
* Pandas: read, filter (department / marks / result), sort, top-5 merit list, department summary
* Matplotlib: marks bar chart (pass/fail colours, average line), grade pie chart, department chart
* HTML: generate a result sheet and extract title, headings, links and table data
* Input validation, grade + pass/fail calculation
