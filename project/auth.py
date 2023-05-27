from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db, app

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/admin')
def login_admin():
    return render_template('loginAdmin.html')

@auth.route('/admin', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password and compare it with the stored password
    if not user or not (user.password == password):
        flash('Please check your login details and try again.')
        app.logger.warning("User login failed")
        return redirect(url_for('auth.login_admin')) # if the user doesn't exist or password is wrong, reload the page
    if (user.user_type != 'admin'):
        flash('You are not admin')
        return redirect(url_for('auth.login_admin'))

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.showRestaurants'))

@auth.route('/restaurantOwner')
def login_owner():
    return render_template('loginOwner.html')

@auth.route('/restaurantOwner', methods=['POST'])
def login_owner_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password and compare it with the stored password
    if not user or not (user.password == password):
        flash('Please check your login details and try again.')
        app.logger.warning("User login failed")
        return redirect(url_for('auth.login_owner')) # if the user doesn't exist or password is wrong, reload the page
    if (user.user_type != 'res_owner'):
        flash('You are not owner')
        return redirect(url_for('auth.login_owner'))

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.showRestaurants'))

@auth.route('/customer')
def login_customer():
    return render_template('loginCustomer.html')

@auth.route('/customer', methods=['POST'])
def login_customer_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password and compare it with the stored password
    if not user or not (user.password == password):
        flash('Please check your login details and try again.')
        app.logger.warning("User login failed")
        return redirect(url_for('auth.login_customer')) # if the user doesn't exist or password is wrong, reload the page
    
    #checking customer type
    if (user.user_type != 'customer'):
        flash('You are not customer')
        app.logger.warning("User login failed")
        return redirect(url_for('auth.login_customer')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.showRestaurants'))

@auth.route('/logout')
@login_required
def logout():
    logout_user();
    return redirect(url_for('main.showRestaurants'))