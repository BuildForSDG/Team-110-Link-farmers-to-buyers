from flask import Flask
from flask_sqlalchemy import SQLAlchemy #import SQLAlchemy
import json
from datetime import datetime
from settings import app 

db = SQLAlchemy(app)

class User(db.Model):
    '''User class with table user'''
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(11), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    role = db.Column(db.String(10), nullable=False, default='Buyer') #setting default role to buyer if not farmer
    profile = db.relationship('Profile', backref='user_profile', uselist=False, lazy=True)
    #creating a one to one relationship between the User and Profile
    #Profile as the first parameter reps the Class Profile to which it's linked to
    #backref creates a false column in the Profile class with name 'user_profile'
    #uselist is false for one to one relationship because if you can't have a list, then the
    # you can only have one value
    order = db.relationship('Order', backref='user_order', lazy=True) 
        
    def json(self):
        return {'id': self.id, 'full_name': self.full_name, 'Phone_number': self.phone, 
                'Email': self.email, 'profile_picture':self.profile_picture, 
                'Farm_name': self.farm_name, 'Farm_Location': self.farm_location}
        
    def add_Farmer(_phone, _full_name, _password, _email):
        '''fuction to add farmer to the database'''
        new_farmer = Farmer(phone=_phone, full_name=_full_name, password=_password, email=_email)
        db.session.add(new_farmer) #add new farmer to database
        db.session.commit() # committing changes

    def getAllFarmers():
        '''function to return all farmers in the database'''
        return [Farmer.json(i) for i in Farmer.query.all()]

    def getFarmer(_phone):
        '''function to get a farmer's profile using phone number as parameter'''
        #return [Farmer.json(i) for i in Farmer.query.filter_by(phone=_phone).first()]
        return Farmer.json(Farmer.query.filter_by(phone=_phone).first())

    def editFarmer(_phone, _full_name, _password, _profile_picture, _farm_name, _farm_location, _email):
        '''Function to edit a Farmer's profile'''
        farmer_to_update = Farmer.query.filter_by(phone=_phone).first()
        farmer_to_update.full_name = _full_name
        farmer_to_update.phone = _phone
        farmer_to_update.password = _password
        farmer_to_update.profile_picture = _profile_picture
        farmer_to_update.farm_name = _farm_name
        farmer_to_update.farm_location = _farm_location
        farmer_to_update.email = _email
        db.session.commit() #commit changes

    def deleteFarmer(_phone):
        '''function to delete a farmer's profile'''
        is_successful = Farmer.query.filter_by(phone=_phone).delete() #filter by phone number and delete
        db.session.commit() #commiting the new change to our database
        return bool(is_successful) #checks if deletion is successful, if successful, it will return an integer
       
    def __repr__(self):
        farmer_object = {
            'id': self.id, 
            'full_name': self.full_name, 
            'Phone_number': self.phone, 
            'Email': self.email, 
            'profile_picture':self.profile_picture, 
            'Farm_name': self.farm_name, 
            'Farm_Location': self.farm_location
        }
        return json.dumps(farmer_object)

class Farm(db.Model):
    '''Farm class with table user'''
    __tablename__ = 'farm'
    id = db.Column(db.Integer, primary_key=True)
    farm_name = db.Column(db.String(80))
    farm_location = db.Column(db.String(80))
    profile_id = db.relationship('Profile', backref='user_farm', lazy=True)
    # one to many relationship between farm and profile

class Profile(db.Model):
    '''Profile class with table user'''
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    profile_picture = db.Column(db.String(80), default='profile.jpg')
    location = db.Column(db.String(80), default='')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farm.id'))
    #false columns user_farm and user_profile exists

class Order(db.Model):
    '''Order class with table order'''
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) #no bracket added after the datetime.utcnow so it wont use the current time as at the creation of this app as default time
    #order_details = db.relationship('OrderDetails', backref='order_item')
    #false columns user_order exists