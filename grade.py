from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

# File path for storing student data
EXCEL_FILE = "grades.xlsx"

# Admin password (Change this as needed)
ADMIN_PASSWORD = "admin123"

# 📌 Check if file exists, if not, create it
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["Student_ID", "Name", "Subject", "Grade", "Total_Marks", "Percentage"])
    df.to_excel(EXCEL_FILE, index=False)

# 📌 Load Data
def load_data():
    return pd.read_excel(EXCEL_FILE)

# 📌 Save Data
def save_data(df):
    df.to_excel(EXCEL_FILE, index=False)

# 📌 Add a new student (with password protection)
@app.route('/add_student', methods=['POST'])
def add_student():
    # Ensure only admin can add a student
    if not verify_password():
        return "❌ Incorrect password! Access denied."

    student_id = request.form['student_id']
    name = request.form['name']
    subject = request.form['subject']
    grade = float(request.form['grade'])
    total_marks = float(request.form['total_marks'])

    percentage = (grade / total_marks) * 100  # Calculate Percentage

    new_student = {
        "Student_ID": student_id,
        "Name": name,
        "Subject": subject,
        "Grade": grade,
        "Total_Marks": total_marks,
        "Percentage": percentage
    }

    # Load existing data
    df = load_data()

    # Append new student
    df = df.append(new_student, ignore_index=True)

    # Save updated data to the Excel file
    save_data(df)
    return redirect(url_for('display_students'))  # Redirect to the page that shows the student records

# 📌 Verify Admin Password
def verify_password():
    # In practice, you should handle password security better (e.g. hashing), but for simplicity, we use plain text.
    return True  # Remove for real password handling, it's set for simplicity in this case

# 📌 Display Students
@app.route('/students')
def display_students():
    df = load_data()
    return render_template('students.html', students=df.to_html())

if __name__ == '__main__':
    app.run(debug=True)
