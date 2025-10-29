# 🎓 MST Marks Analyzer (Python + MySQL + DAA Integration)

## 📘 Project Overview

**MST Marks Analyzer** is a Python-based academic project that automates the process of **Mid-Semester Test (MST)** marks analysis.
It connects Python with a **MySQL database** to store student records, computes **totals, averages, and grades**, ranks students using the **Merge Sort algorithm (DAA)**, and generates **visual charts and a detailed PDF report**.

This project bridges **theoretical concepts from Design and Analysis of Algorithms (DAA)** with **practical applications in data management and visualization**.

---

## 🧩 Features

✅ Connects Python with MySQL for data storage
✅ Calculates total, average, and grade automatically
✅ Implements **Merge Sort Algorithm** for ranking
✅ Generates **bar and pie charts** using Matplotlib
✅ Exports a **PDF report** with summary tables and visualizations
✅ Subject-wise marks comparison and ranking table
✅ Clean, modular, and well-documented code

---

## 🧠 Technologies Used

| Component                | Technology                                          |
| ------------------------ | --------------------------------------------------- |
| **Programming Language** | Python 3                                            |
| **Database**             | MySQL                                               |
| **Libraries**            | NumPy, Matplotlib, FPDF2, mysql.connector           |
| **Algorithm Used**       | Merge Sort (from Design and Analysis of Algorithms) |
| **IDE**                  | Visual Studio Code                                  |
| **Operating System**     | Windows 10 / 11                                     |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/MST-Marks-Analyzer.git
cd MST-Marks-Analyzer
```

### 2️⃣ Install Required Libraries

Make sure you have Python installed (3.10+ recommended).
Then install dependencies using pip:

```bash
pip install mysql-connector-python numpy matplotlib fpdf2
```

### 3️⃣ Setup MySQL Database

Open **MySQL Workbench** and run:

```sql
CREATE DATABASE project;
USE project;

CREATE TABLE mst_marks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    adbms FLOAT,
    hpc FLOAT,
    daa FLOAT,
    python FLOAT
);
```

### 4️⃣ Update MySQL Credentials in the Code

In your Python file:

```python
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="your_password_here",
    database="project"
)
```

### 5️⃣ Run the Project

```bash
python MST_Marks_Analyzer_Final.py
```

---

## 🧮 Sample Input

```
Enter number of students: 3

Enter details for Student 1
Name: Kartik
ADBMS Marks (out of 20): 19
HPC Marks (out of 20): 18
DAA Marks (out of 20): 17
Python Marks (out of 20): 20

Enter details for Student 2
Name: Parv
ADBMS Marks (out of 20): 15
HPC Marks (out of 20): 14
DAA Marks (out of 20): 16
Python Marks (out of 20): 15

Enter details for Student 3
Name: Manya
ADBMS Marks (out of 20): 11
HPC Marks (out of 20): 10
DAA Marks (out of 20): 9
Python Marks (out of 20): 8
```

---

## 📊 Output Features

* ✅ Student-wise and subject-wise summary tables
* ✅ Ranking table (using Merge Sort)
* ✅ Bar and pie charts
* ✅ PDF report automatically saved at `Y:\PROJECT\MST_Marks_Report.pdf`

Example PDF contents:

* Cover Page
* Student Performance Summary
* Grade Distribution
* Ranking Table
* Subject-wise Table and Graphs
* Final Bar & Pie Charts

---

## 📈 Screenshots (Suggested)

You can include:

* Terminal output
* Bar graph (Average comparison)
* Pie chart (Grade distribution)
* Subject-wise charts
* PDF report preview

---

## 🧠 Concepts Applied

* **Database Connectivity:** Python ↔ MySQL integration
* **Algorithm Implementation:** Merge Sort for ranking
* **Visualization:** Matplotlib for chart creation
* **Automation:** PDF generation with FPDF2
* **File Handling & Cleanup:** Auto-save and delete temporary files

---

## 🚀 Future Enhancements

* Add a **GUI interface** using Tkinter or PyQt5
* Create a **web version** using Flask/Django
* Enable **Excel/CSV import** for bulk data
* Email PDF reports to students automatically
* Add **login system** for faculty authentication

---

## 🧾 Author

👨‍💻 **Kartik**
📚 MCA Department
🏫 University of Computing
📅 Project Duration: September – October 2025

---

## 📜 License

This project is created for educational purposes and is free to use and modify.
If you use or reference this code, please credit the author.

---

### ⭐ Show Some Support!

If you found this project helpful, don’t forget to **star ⭐ the repository** on GitHub!

---

Would you like me to generate a **README.md file** version of this (ready to upload to GitHub) and also include your **screenshots placeholders** and **badges** (like “Python”, “MySQL”, “DAA” icons at the top)?
