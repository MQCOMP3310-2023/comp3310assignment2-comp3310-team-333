from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique = True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    user_type = db.Column(db.String(100))

    @property
    def serialize(self):
        return {
            'email'     : self.email,
            'name'      : self.name,
            'id'        : self.id,
            'password'  : self.password,
            'user_type' : self.user_type
        }

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
       }
 
class MenuItem(db.Model):
    name = db.Column(db.String(80), nullable = False)
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(250))
    price = db.Column(db.String(8))
    course = db.Column(db.String(250))
    restaurant_id = db.Column(db.Integer,db.ForeignKey('restaurant.id'))
    restaurant = db.    relationship(Restaurant)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'       : self.name,
           'description' : self.description,
           'id'         : self.id,
           'price'      : self.price,
           'course'     : self.course,
       }