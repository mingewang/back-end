from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer)
    posts = db.relationship('Post', backref='author', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    published_at = db.Column(db.DateTime, default=db.func.current_timestamp())


# create db
#db.create_all()
#print("Database tables created.")

@app.route('/')
def index():
    users = User.query.all()
    posts = Post.query.join(User).add_columns(Post.id, Post.title, Post.content, User.name).all()
    return render_template('blog_index.html', users=users, posts=posts)

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        new_user = User(name=name, email=email, age=age)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    return render_template('create_user.html')


@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    users = User.query.all()
    if request.method == 'POST':
        user_id = request.form['user_id']
        title = request.form['title']
        content = request.form['content']
        new_post = Post(user_id=user_id, title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/')
    return render_template('create_post.html', users=users)



if __name__ == "__main__":
    app.run(debug=True)