from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create User data
user1 = User(name="veena", password="veena123")

session.add(user1)
session.commit()

user2 = User(name="vidya", password="vidya123")

session.add(user2)
session.commit()

user3 = User(name="prajila", password="prajila123")

session.add(user3)
session.commit()

user4 = User(name="dhanya", password="dhanya123")

session.add(user4)
session.commit()

user5 = User(name="sanjna", password="sanjna123")

session.add(user5)
session.commit()

user6 = User(name="kavana", password="kavana123")

session.add(user6)
session.commit()

user7 = User(name="prasad", password="prasad123")

session.add(user7)
session.commit()

user8 = User(name="nadeem", password="nadeem123")

session.add(user8)
session.commit()

# end of user table rows

# Category for Mobiles
category1 = Category(name="Mobiles")

session.add(category1)
session.commit()

# items for Mobile
item1 = Item(
    name="Samsung Galaxy Note 7",
    description="The new stylish phone from Samsung",
    category=category1,
    user=user1)

session.add(item1)
session.commit()

item2 = Item(
    name="Redmi Y2",
    description="The new black phone with 32GB storage",
    category=category1,
    user=user2)

session.add(item2)
session.commit()

# Category for Laptops
category2 = Category(name="Laptops")

session.add(category2)
session.commit()

# items for Laptops
item1 = Item(
    name="Apple MacBook",
    description="MacBook Air Core 13.3-inch Laptop",
    category=category2,
    user=user3)

session.add(item1)
session.commit()


# Category for Tablets
category3 = Category(name="Tablets")

session.add(category3)
session.commit()

# items for Tablets
item1 = Item(
    name="Lenovo Tab",
    description="Tab-4 8 Plus Tablet with Android",
    category=category3,
    user=user4)

session.add(item1)
session.commit()

# Category for Pendrives
category4 = Category(name="Pendrives")

session.add(category4)
session.commit()

# items for Pendrive
item1 = Item(
    name="SanDisk",
    description="SanDisk Cruzer Blade 32GB USB",
    category=category4,
    user=user5)

session.add(item1)
session.commit()

# Category for Wearables
category5 = Category(name="Wearables")

session.add(category5)
session.commit()

# items for Wearables
item1 = Item(
    name="Mi band",
    description="Mi Fit band black",
    category=category5,
    user=user6)

session.add(item1)
session.commit()

# Category for SmartAssysts
category6 = Category(name="SmartAssysts")

session.add(category6)
session.commit()

# items for SmartAssysts
item1 = Item(
    name="Amazon Echo",
    description="Amazon Smart speaker with Alexa Powered by Dolby Black",
    category=category6,
    user=user7)

session.add(item1)
session.commit()

# Category for PowerBanks
category7 = Category(name="PowerBanks")

session.add(category7)
session.commit()

# items for PowerBanks
item1 = Item(
    name="Mi Power bank",
    description="Mi 10000mAH Li-Polymer Power Bank 2i (Black)",
    category=category7,
    user=user8)

session.add(item1)
session.commit()

# READ
firstResult = session.query(Category).first()
print firstResult.name

items = session.query(Item).all()
for item in items:
    print item.name


print "Fetch successful!"
# VB
