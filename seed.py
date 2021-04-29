from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add user
anna = User(first_name='Anna', last_name='Taylor', image_url="https://media.istockphoto.com/photos/cool-guy-in-sunglasses-picture-id153749383")
nate = User(first_name='Nate', last_name='Deakers', image_url="https://media.istockphoto.com/photos/cool-guy-in-sunglasses-picture-id153749383")
lola = User(first_name='Lola', last_name='Taylor', image_url="https://media.istockphoto.com/photos/cool-guy-in-sunglasses-picture-id153749383")

# Add new objects to session, so they'll persist
db.session.add(anna)
db.session.add(nate)
db.session.add(lola)

# Commit--otherwise, this never gets saved!
db.session.commit()