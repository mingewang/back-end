from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


# create engine
engine = create_engine('sqlite:///blog.db', echo=True)
Base = declarative_base()

# define users/post tables
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    age = Column(Integer)
    
    posts = relationship('Post', back_populates='author')

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    
    author = relationship('User', back_populates='posts')

# create tables
Base.metadata.create_all(engine)

# create a session to db
Session = sessionmaker(bind=engine)
session = Session()

# insert/create user to db
new_user = User(name='Alice', email='alice@example.com', age=25)
session.add(new_user)
session.commit()

# create a post
new_post = Post(user_id=new_user.id, title='My First Post', content='Hello, world!')
session.add(new_post)
session.commit()

# query users
users = session.query(User).all()
for user in users:
    print(user.name, user.email, user.age)

# retrieve posts
posts = session.query(Post).join(User).all()
for post in posts:
    print(post.title, post.author.name, post.content)


# update user
user = session.query(User).filter_by(name='Alice').first()
user.age = 26
session.commit()

# delete user
#session.delete(user)
#session.commit()