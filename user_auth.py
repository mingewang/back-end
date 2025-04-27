from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)

# Secret key for sessions
app.secret_key = 'your_secret_key'

# Hardcoded users (In a real app, you'd fetch this from a database)
users = {
    'admin': 'admin123',
    'guest': 'guest123',
}

@app.route('/')
def home():
    # Check if the user is logged in
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validate user credentials
        if username in users and users[username] == password:
            session['username'] = username  # Store username in session
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))

        flash('Invalid username or password!', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)