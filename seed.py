from models import User, db, Post
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

db.session.commit()

# Add posts
post1 = Post(title="My really cool bike", content="Its so fast", user_id=anna.id)
post2 = Post(title="My really cool bike", content="Its so fast", user_id=nate.id)
post3 = Post(title="My really cool bike", content="Its so fast", user_id=lola.id)

db.session.add(post1)
db.session.add(post2)
db.session.add(post3)

# Commit--otherwise, this never gets saved!
db.session.commit()