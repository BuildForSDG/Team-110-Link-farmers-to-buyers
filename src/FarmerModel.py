from flask_sqlalchemy import SQLAlchemy  # import SQLAlchemy
import json
from datetime import datetime
from settings import app

db = SQLAlchemy(app)


class User(db.Model):
    '''User class with table user'''
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(11), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True)
    date_created = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    role = db.Column(db.String(10), nullable=False, default='Buyer')
    # setting default role to buyer if not farmer
    profile_picture = db.Column(db.String(80), default='profile.jpg')
    location = db.Column(db.String(80))
    farm_id = db.Column(db.Integer, db.ForeignKey('farm.id'),
                        nullable=True)
    # We should be able to see the farm a User belongs to through farm id
    # even if the farm name and farm location is None for buyers
    farm = db.relationship('Farm', backref=db.backref('users', lazy=True))
    # I should be able to view all users belonging to a farm from the farmtable

    # order = db.relationship('Order', backref='user_order', lazy=True)

    def json(self):
        return {'id': self.id, 'full_name': self.full_name,
                'Phone_number': self.phone, 'Email': self.email,
                'profile_picture': self.profile_picture,
                'Farm_name': self.farm_name,
                'Farm_Location': self.farm_location,
                'Role': self.role
                }

    def add_User(_phone, _full_name, _password, _email, _role):
        '''fuction to add user to the database'''
        new_user = User(phone=_phone, full_name=_full_name,
                        password=_password, email=_email, role=_role,
                        farm_id=1)
        # setting farm id to be 1, which is None
        db.session.add(new_user)  # add new user to database
        db.session.commit()   # committing changes

    def getAllUsers():
        '''function to view all users in the database'''
        return [User.json(i) for i in User.query.all()]

    def getUser(_phone):
        '''function to get a user's profile using phone number as parameter'''
        return User.json(User.query.filter_by(phone=_phone).first())

    def editUser(_phone, _full_name, _password, _profile_picture,
                 _farm_id, _email):
        '''Function to edit a user's profile'''
        user_to_update = User.query.filter_by(phone=_phone).first()
        user_to_update.full_name = _full_name
        user_to_update.phone = _phone
        user_to_update.password = _password
        user_to_update.profile_picture = _profile_picture
        user_to_update.farm_id = _farm_id
        user_to_update.email = _email
        db.session.commit()  # commit changes

    def deleteUser(_phone):
        '''function to delete a user's profile'''
        is_successful = User.query.filter_by(phone=_phone).delete()
        db.session.commit()  # commiting the new change to our database
        return bool(is_successful)

    def __repr__(self):
        user_object = {
            'id': self.id,
            'full_name': self.full_name,
            'Phone_number': self.phone,
            'Email': self.email,
            'Role': self.role,
            'profile_picture': self.profile_picture,
            'Farm_id': self.farm_id
                       }
        return json.dumps(user_object)


class Farm(db.Model):
    '''Farm class with table farm'''
    __tablename__ = 'farm'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    farm_name = db.Column(db.String(80))
    farm_location = db.Column(db.String(80))

    def json(self):
        return {'id': self.id, 'Farm name': self.farm_name,
                'Farm Location': self.farm_location}

    def add_Farm(_farm_name, _farm_location):
        '''fuction to add farm to the database'''
        new_farm = Farm(farm_name=_farm_name, farm_location=_farm_location)
        db.session.add(new_farm)   # add new farm to database
        db.session.commit()   # committing changes

    def getAllFarm():
        '''function to return all farms in the database'''
        return [Farm.json(i) for i in Farm.query.all()]

    def getFarm(_id):
        '''function to get a farm detail using id as parameter'''
        return Farm.json(Farm.query.filter_by(id=_id).first())

    def editFarm(_id, _farm_name, _farm_location):
        '''Function to edit a Farm'''
        farm_to_update = Farm.query.filter_by(id=_id).first()
        farm_to_update.farm_name = _farm_name
        farm_to_update.farm_location = _farm_location
        db.session.commit()  # commit changes

    def deleteFarm(_id):
        '''function to delete a farmer's profile'''
        is_successful = Farm.query.filter_by(id=_id).delete()
        # filter by farm id and delete
        db.session.commit()   # commiting the new change to our database
        return bool(is_successful)

    def __repr__(self):
        farm_object = {
            'id': self.id,
            'Farm_name': self.farm_name,
            'Farm_Location': self.farm_location
        }
        return json.dumps(farm_object)


class Order(db.Model):
    '''Order class with table order'''
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    order_date = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    orders = db.Column(db.Text)
    # order_details = db.relationship('OrderDetails', backref='order_item')
    # false columns user_order exists
