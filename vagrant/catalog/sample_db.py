from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, Item

engine = create_engine('sqlite:///itemcatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="John Boy", email="johnyboy@fakeemail.com",
             profile_image='http://images.all-free-download.com/images/graphicthumb/cute_puppy_photo_picture_11_168839.jpg')
session.add(User1)
session.commit()

# Book Category
category1 = Category(user_id=1, name="Books")

session.add(category1)
session.commit()

item1 = Item(user_id=1, name="Extreme Ownership", description="Jocko's story of leadership in the Navy SEALs and biznazz",
                     category=category1)

session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Zero to One", description="Peter Thiel's tale of how to build a company",
                     category=category1)

session.add(item2)
session.commit()

# Dessert Category
category2 = Category(user_id=1, name="Songs")

session.add(category2)
session.commit()

item1 = Item(user_id=1, name="Despacito", description="Luis Fonso's summer jammie",
                     category=category2)

session.add(item1)
session.commit()


print "Populated the db with some sample ish!"
