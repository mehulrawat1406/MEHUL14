from flask import Flask
app = Flask(__name__)  # Creating a Flask app instance

from flask import redirect, render_template, session, url_for

@app.route('/modified')
def modified():
    if 'user' in session and session['user']:  # Ensure session exists and is not empty
        print(f"✅ User found in session: {session['user']}")  # Debugging log
        return render_template('modified.html', user=session['user'])
    else:
        print("🔴 No user found in session. Redirecting to SignUp.")  # Debugging log
        return redirect(url_for('SignUp'))  # Redirect to SignUp if not logged in
if __name__ == '__main__':
        app.run(debug=True)
