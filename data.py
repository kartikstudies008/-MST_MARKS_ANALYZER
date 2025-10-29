# 🎓 MCA PROJECT – MST Marks Analyzer (MySQL + PDF Version)
# Author: Kartik
# Description: Inserts marks into MySQL, fetches data, analyzes results, and generates a PDF report.

import mysql.connector
from fpdf import FPDF
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

# --- Step 1: Connect to MySQL ---
conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="16.13@Ka",   # 🔒 your password
    database="project"      # existing database
)

if conn.is_connected():
    print("✅ Connected successfully to MySQL Workbench database!")

cursor = conn.cursor()

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

# --- Step 5: Create and Save Graphs ---
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

# --- Step 6: Generate PDF Report ---
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_doc_option("core_fonts_encoding", "utf-8")

# COVER PAGE
pdf.add_page()
pdf.set_font("Arial", 'B', 20)
pdf.cell(200, 10, "MCA PROJECT REPORT", ln=True, align='C')
pdf.ln(10)
pdf.set_font("Arial", 'B', 16)
pdf.cell(200, 10, "MST MARKS ANALYZER (MySQL + Python)", ln=True, align='C')
pdf.ln(10)

pdf.set_font("Arial", '', 12)
pdf.cell(200, 10, f"Generated On: {datetime.now().strftime('%d-%m-%Y %I:%M %p')}", ln=True, align='C')
pdf.ln(15)

pdf.multi_cell(0, 10, 
    "This project connects Python with MySQL to store and analyze MST marks. "
    "It calculates averages, assigns grades, and generates visual charts "
    "and a professional report.\n\n"
    "Database: project\nTable: mst_marks\n"
    "Developed by: Kartik"
)
pdf.ln(20)

# --- Step 7: Add Data Summary ---
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

# --- Step 8: Grade Distribution Summary ---
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

# --- Step 9: Add Graphs to PDF ---
pdf.ln(10)
pdf.set_font("Arial", 'B', 14)
pdf.cell(0, 10, "VISUAL ANALYSIS", ln=True)
pdf.ln(5)
pdf.image(bar_chart_path, x=30, w=150)
pdf.ln(5)
pdf.image(pie_chart_path, x=40, w=130)

# --- Step 10: Save PDF to Y:\PROJECT ---
output_path = r"Y:\PROJECT\MST_Marks_Report.pdf"
pdf.output(output_path)
print(f"\n✅ PDF Report generated successfully at:\n{output_path}")

# --- Step 11: Auto-open PDF (Windows only) ---
try:
    os.startfile(output_path)
except Exception as e:
    print(f"⚠️ Could not auto-open PDF: {e}")

# --- Step 12: Clean up ---
os.remove(bar_chart_path)
os.remove(pie_chart_path)
cursor.close()
conn.close()
print("\n📁 MySQL connection closed and report complete.")
