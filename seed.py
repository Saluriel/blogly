from models import User, db
from app import app

db.drop_all()
db.create_all()

User.query.delete()

Linda = User(first_name='Linda', last_name='H')
Brad = User(first_name='Brad', last_name='fdsafsdafsda')
Gregory = User(first_name='Gregory', last_name='FSDAFASDF')
SomeGuy = User(first_name='SomeGuy', last_name='?????')
RandomPerson = User(first_name='!!!!!!', last_name='!!!!!!')

db.session.add(Linda)
db.session.add(Brad)
db.session.add(Gregory)
db.session.add(SomeGuy)
db.session.add(RandomPerson)


db.session.commit()