from models import User, db, Post, Tag, PostTag
from app import app

db.drop_all()
db.create_all()

User.query.delete()

Linda = User(first_name='Linda', last_name='B', image_url='https://upload.wikimedia.org/wikipedia/commons/2/2b/Jessica_Ennis_%28May_2010%29_cropped.jpg')
Brad = User(first_name='Brad', last_name='A', image_url='https://m.media-amazon.com/images/M/MV5BMjA1MjE2MTQ2MV5BMl5BanBnXkFtZTcwMjE5MDY0Nw@@._V1_.jpg')
Gregory = User(first_name='Gregory', last_name='C')
SomeGuy = User(first_name='SomeGuy', last_name='Z')
RandomPerson = User(first_name='!!!!!!', last_name='D')

db.session.add(Linda)
db.session.add(Brad)
db.session.add(Gregory)
db.session.add(SomeGuy)
db.session.add(RandomPerson)

db.session.commit()


p1 = Post(title='Test1', content='I found a really cool rock today', user_id=1)
p2 = Post(title='Test2', content='fjkdlsajfdlas', user_id=1)
p3 = Post(title='Test3', content='fjkdlsajfdlas', user_id=1)
p4 = Post(title='Test4', content='fjkdlsajfdlas', user_id=1)

db.session.add_all([p1, p2, p3, p4])

db.session.commit()

t1 = Tag(name='#cool')
t2 = Tag(name='#lol')
t3 = Tag(name='#test')

db.session.add_all([t1, t2, t3])
db.session.commit()

pt1 = PostTag(post_id=1, tag_id=1)
pt2 = PostTag(post_id=1, tag_id=2)
pt3 = PostTag(post_id=2, tag_id=3)
pt4 = PostTag(post_id=2, tag_id=1)

db.session.add_all([pt1, pt2, pt3, pt4])
db.session.commit()

