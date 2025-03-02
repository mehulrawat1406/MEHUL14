from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os
import bcrypt

app = Flask(__name__)
app.secret_key = 'os.random(24)'  # Required for session management

# Define Excel file path
EXCEL_FILE = "students.xlsx"

# Create students.xlsx if it doesn't exist
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["Student_ID", "Password", "Role"])
    df.to_excel(EXCEL_FILE, index=False)

# Load student data from Excel
def load_students():
    return pd.read_excel(EXCEL_FILE, dtype=str)

# Save student data to Excel
def save_students(df):
    df.to_excel(EXCEL_FILE, index=False)

@app.route('/')
def home():
    return redirect(url_for('SignUp'))  # Redirect to SignUp page

@app.route('/SignUp', methods=['GET', 'POST'])
def SignUp():
    if request.method == 'POST':
        role = request.form.get('role')
        student_id = request.form.get('userID')
        password = request.form.get('password')

        if not student_id or not password:
            return render_template('signup.html', error="❌ Please enter both Student ID and Password.")

        # Hash the password before storing
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Load existing data
        df = load_students()

        # Check if student ID already exists
        if student_id in df["Student_ID"].astype(str).values:
            return render_template('signup.html', error="❌ Student ID already exists.")

        # Append new student
        new_student = pd.DataFrame({
            "Student_ID": [student_id], 
            "Password": [hashed_password.decode('utf-8')],
            "Role": [role]
        }).astype(str)
        
        df = pd.concat([df, new_student], ignore_index=True)

        # Save updated data
        save_students(df)

        # Store student ID in session
        session['user'] = student_id

        print(f"✅ User {student_id} signed up successfully!")  # Debugging log
        return redirect(url_for('modified'))  # Redirect to modified.html

    return render_template('signup.html')


@app.route('/modified')
def modified():
    if 'user' in session:
        return render_template('modified.html', user=session['user'])
    else:
        return redirect(url_for('home'))  # Redirect to SignUp if not logged in

if __name__ == '__main__':
        app.run(debug=True)


