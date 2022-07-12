from models import User, db
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