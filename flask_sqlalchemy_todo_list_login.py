from flask import Flask, request, render_template, redirect, url_for, session, flash    
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'todo.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
# Secret key for sessions
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    todos = db.relationship('Todo', backref='author', lazy=True)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    published_at = db.Column(db.DateTime, default=db.func.current_timestamp())


# create db
#db.create_all()
#print("Database tables created.")

@app.route('/')
def home():
    # Check if the user is logged in
    if 'username' in session:
        username = session['username']
        # Fetch user and their posts from the database
        user = User.query.filter_by(name=username).first()
        todos = user.todos if user else []
        return render_template('todo_index.html', username=username, todos=todos)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # check if the user exists in the database
        user = User.query.filter_by(name=username).first()
        if user and user.password == password:
            session['username'] = username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        flash('Invalid username or password!', 'danger')
    return render_template('todo_login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        password = request.form['password']
        new_user = User(name=name, email=email, age=age, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    return render_template('todo_register.html')


@app.route('/create_todo', methods=['GET', 'POST'])
def create_todo():
    if 'username'  not in session:
        flash('You need to log in first!', 'warning')
        return redirect(url_for('login'))
    # Check if the user is logged in
    username = session['username']
    user = User.query.filter_by(name=username).first()
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('login'))
    # Fetch all users for the dropdown
    #users = User.query.all()
    if request.method == 'POST':
        user_id = request.form['user_id']
        title = request.form['title']
        content = request.form['content']
        new_todo = Todo(user_id=user_id, title=title, content=content)
        db.session.add(new_todo)
        db.session.commit()
        return redirect('/')

    # create a new todo form
    return render_template('todo_create.html', user=user)

# before run 
#  mv migrations/ migrations_blog
#  flask --app flask_sqlalchemy_todo_list_login.py db init
#  flask --app flask_sqlalchemy_todo_list_login.py db migrate -m "initila migrate"
#  flask --app flask_sqlalchemy_todo_list_login.py db upgrade
if __name__ == "__main__":
    app.run(debug=True)