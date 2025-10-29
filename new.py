# 🎓 MCA PROJECT – MST Marks Analyzer (Python + MySQL Integration)
# Author: Your Name
# Database: project

import mysql.connector
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

# --- Step 1: Connect to MySQL Workbench ---
conn = mysql.connector.connect(
    host="127.0.0.1",         # localhost
    port=3306,                # default port
    user="root",              # your MySQL username
    password="16.13@Ka",      # 🔒 replace with your MySQL password
    auth_plugin='mysql_native_password'
)
cursor = conn.cursor()

# --- Step 2: Create Database and Table Automatically ---
cursor.execute("CREATE DATABASE IF NOT EXISTS project")
cursor.execute("USE project")
cursor.execute("""
CREATE TABLE IF NOT EXISTS mst_marks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    adbms FLOAT,
    hpc FLOAT,
    daa FLOAT,
    python FLOAT
)
""")
print("✅ Connected & Database/Table 'project.mst_marks' ready!")

# --- Step 3: Input Student Data ---
n = int(input("\nEnter number of students: "))
for i in range(n):
    print(f"\n📘 Enter details for Student {i+1}")
    name = input("Name: ")
    adbms = float(input("ADBMS Marks (out of 20): "))
    hpc = float(input("HPC Marks (out of 20): "))
    daa = float(input("DAA Marks (out of 20): "))
    python = float(input("Python Marks (out of 20): "))

    cursor.execute(
        "INSERT INTO mst_marks (name, adbms, hpc, daa, python) VALUES (%s,%s,%s,%s,%s)",
        (name, adbms, hpc, daa, python)
    )
    conn.commit()

print("\n✅ All data inserted successfully into MySQL database!")

# --- Step 4: Fetch Data from SQL ---
cursor.execute("SELECT name, adbms, hpc, daa, python FROM mst_marks")
data = cursor.fetchall()

names, marks = [], []
for row in data:
    names.append(row[0])
    marks.append(row[1:])

marks_array = np.array(marks)

# --- Step 5: Analyze Data ---
averages = np.mean(marks_array, axis=1)
grades = []
for avg in averages:
    if avg >= 18:
        grades.append('A+')
    elif avg >= 15:
        grades.append('A')
    elif avg >= 12:
        grades.append('B')
    elif avg >= 8:
        grades.append('C')
    else:
        grades.append('F')

# --- Step 6: Display Summary in Terminal ---
print("\n📊 MST MARKS SUMMARY 📊")
print("-" * 55)
print(f"{'Name':<15}{'Average':<10}{'Grade':<10}")
print("-" * 55)
for i in range(len(names)):
    print(f"{names[i]:<15}{averages[i]:<10.2f}{grades[i]:<10}")
print("-" * 55)

# --- Step 7: Bar Chart ---
plt.figure(figsize=(10,5))
plt.bar(names, averages, color='lightgreen', edgecolor='black')
plt.xlabel("Students")
plt.ylabel("Average Marks (out of 20)")
plt.title("MST Average Marks Comparison 📊")
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.show(block=False)

# --- Step 8: Pie Chart ---
grade_labels, grade_counts = np.unique(grades, return_counts=True)
plt.figure(figsize=(6,6))
plt.pie(grade_counts, labels=grade_labels, autopct='%1.1f%%',
        colors=['gold','lightgreen','lightskyblue','lightcoral','violet'])
plt.title("Grade Distribution 🍀")
plt.show(block=True)

# --- Step 8.5: Save Project Report to File ---
file_path = r"C:\Users\Kartik\Desktop\project_report.txt"  # ✅ change location if needed

with open(file_path, "w") as f:
    # --- Report Header ---
    f.write("=============================================\n")
    f.write("     MCA PROJECT – MST MARKS ANALYZER REPORT\n")
    f.write("=============================================\n")
    f.write(f"Report Generated On: {datetime.now().strftime('%d-%m-%Y %I:%M %p')}\n")
    f.write("Database: project\n")
    f.write("Table: mst_marks\n")
    f.write("-" * 55 + "\n\n")

    # --- Student Details ---
    f.write("📘 STUDENT PERFORMANCE SUMMARY\n")
    f.write("-" * 55 + "\n")
    f.write(f"{'Name':<15}{'Average':<10}{'Grade':<10}\n")
    f.write("-" * 55 + "\n")
    for i in range(len(names)):
        f.write(f"{names[i]:<15}{averages[i]:<10.2f}{grades[i]:<10}\n")
    f.write("-" * 55 + "\n")

    # --- Grade Distribution ---
    f.write("\n📊 GRADE DISTRIBUTION\n")
    total_students = len(names)
    for g, c in zip(grade_labels, grade_counts):
        f.write(f"Grade {g}: {c} student(s) ({(c/total_students)*100:.1f}%)\n")
    f.write("-" * 55 + "\n")
    f.write(f"Total Students: {total_students}\n")

    # --- SQL Info ---
    f.write("\n🗄️ Data successfully stored in MySQL Database 'project.mst_marks'\n")
    f.write("You can verify using: SELECT * FROM project.mst_marks;\n")

print(f"\n✅ Full project report saved successfully at:\n{file_path}")

# --- Optional: Auto-open report after save (Windows only) ---
try:
    os.startfile(file_path)
except Exception as e:
    print(f"⚠️ Could not auto-open file: {e}")

# --- Step 9: Close MySQL Connection ---
cursor.close()
conn.close()
print("\n🔒 MySQL connection closed safely.")
