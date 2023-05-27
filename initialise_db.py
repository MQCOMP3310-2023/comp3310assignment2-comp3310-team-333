from project import db, create_app, models
from project.models import User, MenuItem, Restaurant

def populate_db():

    session = db.session()

    session.query(User).delete()
    session.commit()

    session.query(MenuItem).delete()
    session.commit()

    session.query(Restaurant).delete()
    session.commit()

    print("Items have cleaned")

    # Adding admin
    admin = User(email = "admin@admin.com", name = "Admin", password = "1234", user_type = "admin")
    session.add(admin)
    session.commit()

    print("Admin has added")
    
    # Adding restaurant owenr
    user1 = User(email = "jhon@gmail.com", name = "Jhon", password = "1234", user_type = "res_owner")
    session.add(user1)
    session.commit()

    # Adding customer
    user2 = User(email = "smith@gmail.com", name = "Smith", password = "1234", user_type = "customer")
    session.add(user2)
    session.commit()

    print("Users have added")

    #Adding Restaurant and its menu items
    restaurant1 = Restaurant(name = "Urban Burger", user = user1)
    session.add(restaurant1)
    session.commit()
    
    menuItem1 = MenuItem(name = "French Fries", description = "with garlic and parmesan", price = "$2.99", course = "Appetizer", restaurant = restaurant1)
    session.add(menuItem1)
    session.commit()
    
    menuItem2 = MenuItem(name = "Chicken Burger", description = "Juicy grilled chicken patty with tomato mayo and lettuce", price = "$5.50", course = "Entree", restaurant = restaurant1)
    session.add(menuItem2)
    session.commit()

    print("Restaurant and Menu Items have added")

if __name__ == '__main__':
  app = create_app()
  with app.app_context():
    db.drop_all()
    db.create_all()
    populate_db()

