from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Restaurant, MenuItem, User, rates
from sqlalchemy import asc, text, exc
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
   return render_template('main.html')

#Show all restaurants
@main.route('/restaurant/')
@login_required
def showRestaurants():
  restaurants = db.session.query(Restaurant).order_by(asc(Restaurant.name))
  return render_template('restaurants.html', restaurants = restaurants, type = current_user.user_type, name = current_user.name)

#Create a new restaurant
@main.route('/restaurant/new/', methods=['GET','POST'])
@login_required
def newRestaurant():
    if current_user.user_type != 'customer':
        if request.method == 'POST':
            safe_name = text(request.form['name'])
            newRestaurant = Restaurant(name = str(safe_name), user_id = current_user.id)
            db.session.add(newRestaurant)
            flash('New Restaurant %s Successfully Created' % newRestaurant.name)
            db.session.commit()
            return redirect(url_for('main.showRestaurants'))
        else:
            return render_template('newRestaurant.html')
    else: 
       return redirect(url_for('main.showRestaurants'))

#Edit a restaurant
@main.route('/restaurant/<int:restaurant_id>/edit/', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant = db.session.query(Restaurant).filter_by(id = restaurant_id).one()
    if current_user.name == 'Admin' or current_user.id == restaurant.user_id:
        editedRestaurant = db.session.query(Restaurant).filter_by(id = restaurant_id).one()
        if request.method == 'POST':
            if request.form['name']:
                safe_name = request.form['name']
                editedRestaurant.name = str(safe_name)
                flash('Restaurant Successfully Edited %s' % editedRestaurant.name)
                db.session.add(editedRestaurant)
                db.session.commit() 
                return redirect(url_for('main.showRestaurants'))
        else:
            return render_template('editRestaurant.html', restaurant = editedRestaurant)
    else: 
       return redirect(url_for('main.showRestaurants'))    



#Delete a restaurant
@main.route('/restaurant/<int:restaurant_id>/delete/', methods = ['GET','POST'])
def deleteRestaurant(restaurant_id):
    restaurant = db.session.query(Restaurant).filter_by(id = restaurant_id).one()
    if current_user.name == 'Admin' or current_user.id == restaurant.user_id:
        restaurantToDelete = db.session.query(Restaurant).filter_by(id = restaurant_id).one()
        if request.method == 'POST':
            db.session.delete(restaurantToDelete)
            flash('%s Successfully Deleted' % restaurantToDelete.name)
            db.session.commit()
            return redirect(url_for('main.showRestaurants', restaurant_id = restaurant_id))
        else:
            return render_template('deleteRestaurant.html',restaurant = restaurantToDelete)
    else: 
       return redirect(url_for('main.showRestaurants'))   

#Shows restaurant menu
#Shows restaurant rating
@main.route('/restaurant/<int:restaurant_id>/')
@main.route('/restaurant/<int:restaurant_id>/menu/')
@login_required
def showMenu(restaurant_id):
    restaurant = db.session.query(Restaurant).filter_by(id = restaurant_id).one()

    ratings =  db.session.query(rates).filter_by(res_id=restaurant_id).all()
    rating = round(sum([rating.rating for rating in ratings])/len(ratings), 1) if ratings else 0

    user = db.session.query(User).filter_by(id = restaurant.user_id).one()
    items = db.session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return render_template('menu.html', items = items, restaurant = restaurant, creater_name = user.name, user_name = current_user.name, rate=rating)
     


#Create a new menu item
@main.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    restaurant = db.session.query(Restaurant).filter_by(id = restaurant_id).one()
    if current_user.name == 'Admin' or current_user.id == restaurant.user_id:
        if request.method == 'POST':
            safe_name = text(request.form['name'])
            safe_desc = text(request.form['description'])
            newItem = MenuItem(name = str(safe_name), description = str(safe_desc), price = request.form['price'], course = request.form['course'], restaurant_id = restaurant_id)
            db.session.add(newItem)
            db.session.commit()
            flash('New Menu %s Item Successfully Created' % (newItem.name))
            return redirect(url_for('main.showMenu', restaurant_id = restaurant_id))
        else:
            return render_template('newmenuitem.html', restaurant_id = restaurant_id)
    else: 
       return redirect(url_for('main.showRestaurants'))

#Edit a menu item
@main.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):

    editedItem = db.session.query(MenuItem).filter_by(id = menu_id).one()
    restaurant = db.session.query(Restaurant).filter_by(id = restaurant_id).one()
    if current_user.name == 'Admin' or current_user.id == restaurant.user_id:
        if request.method == 'POST':
            if request.form['name']:
                safe_name = text(request.form['name'])
                editedItem.name = str(safe_name)
            if request.form['description']:
                safe_desc = text(request.form['description'])
                editedItem.description = str(safe_desc)
            if request.form['price']:
                editedItem.price = request.form['price']
            if request.form['course']:
                editedItem.course = request.form['course']
            db.session.add(editedItem)
            db.session.commit() 
            flash('Menu Item Successfully Edited')
            return redirect(url_for('main.showMenu', restaurant_id = restaurant_id))
        else:
            return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)
    else: 
       return redirect(url_for('main.showRestaurants'))

#Delete a menu item
@main.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods = ['GET','POST'])
def deleteMenuItem(restaurant_id,menu_id):
    restaurant = db.session.query(Restaurant).filter_by(id = restaurant_id).one()
    if current_user.name == 'Admin' or current_user.id == restaurant.user_id:
        itemToDelete = db.session.query(MenuItem).filter_by(id = menu_id).one() 
        if request.method == 'POST':
            db.session.delete(itemToDelete)
            db.session.commit()
            flash('Menu Item Successfully Deleted')
            return redirect(url_for('main.showMenu', restaurant_id = restaurant_id))
        else:
            return render_template('deleteMenuItem.html', item = itemToDelete)
    else: 
       return redirect(url_for('main.showRestaurants'))
    
#Posts ratings
@main.route('/restaurant/<int:restaurant_id>/rate', methods=['POST'])
def rating(restaurant_id):
    if current_user.user_type == "customer":
        try:
            user = db.session.query(rates).filter_by(user_id=current_user.id, res_id=restaurant_id).one()
        except exc.NoResultFound:
            new_rating = rates(user_id=current_user.id, res_id=restaurant_id, rating=request.form['star'])
            db.session.add(new_rating)
        else:
            user.rating = request.form['star']
        finally:
            db.session.commit()

    return redirect(url_for('main.showMenu', restaurant_id = restaurant_id))