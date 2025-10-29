# 🎓 MCA PROJECT – MST Marks Analyzer (MySQL + DAA + PDF Version)
# Author: Kartik
# Description: Connects Python with MySQL, analyzes MST marks, ranks using Merge Sort (DAA), and generates PDF.

# --- Imports ---
import mysql.connector
from fpdf import FPDF
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
import warnings

# --- Hide Deprecation Warnings ---
warnings.filterwarnings("ignore")

# --- Step 1: Connect to MySQL ---
conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="16.13@Ka",  # 🔒 Your MySQL password
    database="project"    # Existing database
)

if conn.is_connected():
    print("✅ Connected successfully to MySQL Workbench database!")

cursor = conn.cursor()

# --- Step 1.5: Create Table if Not Exists ---
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

# --- Step 2: Insert Student Data ---
n = int(input("Enter number of students: "))

for i in range(n):
    print(f"\n📘 Enter details for Student {i+1}")
    name = input("Name: ")
    adbms = float(input("ADBMS Marks (out of 20): "))
    hpc = float(input("HPC Marks (out of 20): "))
    daa = float(input("DAA Marks (out of 20): "))
    python = float(input("Python Marks (out of 20): "))

    query = "INSERT INTO mst_marks (name, adbms, hpc, daa, python) VALUES (%s, %s, %s, %s, %s)"
    values = (name, adbms, hpc, daa, python)
    cursor.execute(query, values)
    conn.commit()

print("\n✅ All data inserted successfully into MySQL database!")

# --- Step 3: Fetch All Records from Database ---
cursor.execute("SELECT name, adbms, hpc, daa, python FROM mst_marks")
data = cursor.fetchall()

names = [row[0] for row in data]
marks = [row[1:] for row in data]
marks_array = np.array(marks)

# --- Step 4: Calculate Averages and Grades ---
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

# --- Step 5: DAA Integration - Merge Sort Algorithm for Ranking ---
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i][1] > right_half[j][1]:  # Sort descending
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

# Calculate total marks and sort using Merge Sort
totals = np.sum(marks_array, axis=1)
students_data = list(zip(names, totals))
merge_sort(students_data)

# --- Step 6: Display Ranking in Console ---
print("\n🏆 STUDENT RANKING BASED ON TOTAL MARKS (USING MERGE SORT - DAA)")
print("-" * 55)
print(f"{'Rank':<10}{'Name':<15}{'Total Marks':<10}")
print("-" * 55)
for rank, (name, total) in enumerate(students_data, start=1):
    print(f"{rank:<10}{name:<15}{total:<10.2f}")
print("-" * 55)

# --- Step 7: Create and Save Graphs ---
plt.figure(figsize=(8, 4))
plt.bar(names, averages, color='lightgreen', edgecolor='black')
plt.title("MST Average Marks Comparison")
plt.xlabel("Students")
plt.ylabel("Average Marks (out of 20)")
plt.grid(axis='y', linestyle='--', alpha=0.6)
bar_chart_path = "bar_chart.png"
plt.savefig(bar_chart_path)
plt.close()

grade_labels, grade_counts = np.unique(grades, return_counts=True)
plt.figure(figsize=(5, 5))
plt.pie(grade_counts, labels=grade_labels, autopct='%1.1f%%',
        colors=['gold', 'lightgreen', 'lightskyblue', 'lightcoral', 'violet'])
plt.title("Grade Distribution")
pie_chart_path = "pie_chart.png"
plt.savefig(pie_chart_path)
plt.close()

# --- Step 8: Generate PDF Report ---
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)

# COVER PAGE
pdf.add_page()
pdf.set_font("Arial", 'B', 20)
pdf.cell(200, 10, "MCA PROJECT REPORT", ln=True, align='C')
pdf.ln(10)
pdf.set_font("Arial", 'B', 16)
pdf.cell(200, 10, "MST MARKS ANALYZER (MySQL + DAA + Python)", ln=True, align='C')
pdf.ln(10)

pdf.set_font("Arial", '', 12)
pdf.cell(200, 10, f"Generated On: {datetime.now().strftime('%d-%m-%Y %I:%M %p')}", ln=True, align='C')
pdf.ln(15)

pdf.multi_cell(0, 10,
    "This project connects Python with MySQL to store and analyze MST marks. "
    "It calculates averages, assigns grades, ranks students using the Merge Sort algorithm from DAA, "
    "and generates visual charts and a professional report.\n\n"
    "Database: project\nTable: mst_marks\n"
    "Developed by: Kartik"
)
pdf.ln(20)

# --- Student Summary ---
pdf.add_page()
pdf.set_font("Arial", 'B', 14)
pdf.cell(0, 10, "STUDENT PERFORMANCE SUMMARY", ln=True)
pdf.ln(5)

pdf.set_font("Arial", 'B', 12)
pdf.cell(60, 10, "Name", 1)
pdf.cell(40, 10, "Average", 1)
pdf.cell(40, 10, "Grade", 1)
pdf.ln()

pdf.set_font("Arial", '', 12)
for i in range(len(names)):
    pdf.cell(60, 10, names[i], 1)
    pdf.cell(40, 10, f"{averages[i]:.2f}", 1)
    pdf.cell(40, 10, grades[i], 1)
    pdf.ln()

# --- Grade Distribution ---
pdf.ln(10)
pdf.set_font("Arial", 'B', 14)
pdf.cell(0, 10, "GRADE DISTRIBUTION", ln=True)
pdf.ln(5)
pdf.set_font("Arial", '', 12)
total_students = len(names)
for g, c in zip(grade_labels, grade_counts):
    percent = (c / total_students) * 100
    pdf.cell(0, 8, f"Grade {g}: {c} student(s) ({percent:.1f}%)", ln=True)
pdf.ln(5)
pdf.cell(0, 8, f"Total Students: {total_students}", ln=True)

# --- Ranking Table using Merge Sort (DAA) ---
pdf.add_page()
pdf.set_font("Arial", 'B', 14)
pdf.cell(0, 10, "RANKING BASED ON TOTAL MARKS (USING MERGE SORT - DAA)", ln=True)
pdf.ln(5)
pdf.set_font("Arial", 'B', 12)
pdf.cell(40, 10, "Rank", 1)
pdf.cell(60, 10, "Name", 1)
pdf.cell(60, 10, "Total Marks", 1)
pdf.ln()

pdf.set_font("Arial", '', 12)
for rank, (name, total) in enumerate(students_data, start=1):
    pdf.cell(40, 10, str(rank), 1)
    pdf.cell(60, 10, name, 1)
    pdf.cell(60, 10, f"{total:.2f}", 1)
    pdf.ln()

# --- Charts ---
pdf.ln(10)
pdf.set_font("Arial", 'B', 14)
pdf.cell(0, 10, "VISUAL ANALYSIS", ln=True)
pdf.ln(5)
pdf.image(bar_chart_path, x=30, w=150)
pdf.ln(5)
pdf.image(pie_chart_path, x=40, w=130)

# --- Step 9: Save PDF in Y:\PROJECT ---
output_path = r"Y:\PROJECT\MST_Marks_Report.pdf"

# ✅ Ensure the directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

pdf.output(output_path)
print(f"\n✅ PDF Report generated successfully at:\n{output_path}")

# --- Auto-open PDF (Windows only) ---
if os.name == "nt":
    os.startfile(output_path)

# --- Step 10: Cleanup ---
os.remove(bar_chart_path)
os.remove(pie_chart_path)
cursor.close()
conn.close()
print("\n📁 MySQL connection closed and report complete.")
