# 🎓 MST Marks Analyzer (Python + MySQL Integration)
# Author: Your Name
# Description: Stores and analyzes MST marks using MySQL + Python

import mysql.connector
import numpy as np
import matplotlib.pyplot as plt

# --- Step 1: Connect to MySQL Workbench ---
conn = mysql.connector.connect(
    host="127.0.0.1",       # same as in Workbench
    port=3306,              # default port
    user="root",            # MySQL username
    password="16.13@Ka",  # 🔒 replace with your MySQL password
    database="mst"       # your database name
)

if conn.is_connected():
    print("✅ Connected successfully to MySQL Workbench database!")

cursor = conn.cursor()

# --- Step 2: Insert New Student Data ---
n = int(input("\nEnter number of students: "))

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

names = []
marks = []
for row in data:
    names.append(row[0])
    marks.append(row[1:])

marks_array = np.array(marks)

# --- Step 4: Calculate Totals, Averages, and Grades ---
totals = np.sum(marks_array, axis=1)
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

# --- Step 5: Print Summary ---
print("\n📊 MST MARKS SUMMARY 📊")
print("-" * 55)
print(f"{'Name':<15}{'Average':<10}{'Grade':<10}")
print("-" * 55)
for i in range(len(names)):
    print(f"{names[i]:<15}{averages[i]:<10.2f}{grades[i]:<10}")
print("-" * 55)

# --- Step 6: Visualization ---

# --- Bar Chart ---
plt.figure(figsize=(10,5))
plt.bar(names, averages, color='lightgreen', edgecolor='black')
plt.xlabel("Students")
plt.ylabel("Average Marks (out of 20)")
plt.title("MST Average Marks Comparison 📊")
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()  # Adjust layout
plt.show(block=False)  # 👈 Don't block the next plot

# --- Pie Chart ---
grade_labels, grade_counts = np.unique(grades, return_counts=True)
plt.figure(figsize=(6,6))
plt.pie(grade_counts, labels=grade_labels, autopct='%1.1f%%',
        colors=['gold','lightgreen','lightskyblue','lightcoral','violet'])
plt.title("Grade Distribution 🍀")
plt.tight_layout()
plt.show(block=True)  # 👈 Keeps both open properly


# --- Step 7: Close Connection ---
cursor.close()
conn.close()
print("\n🔒 MySQL connection closed safely.")
