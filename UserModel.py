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
    email = db.Column(db.String(80), unique=False)
    date_created = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    role = db.Column(db.String(10), nullable=False, default='Buyer')
    # setting default role to buyer if not farmer
    profile_picture = db.Column(db.String(80), default='profile.jpg')
    location = db.Column(db.String(80))

    # defining foreign key and relationship
    farm_id = db.Column(db.Integer, db.ForeignKey('farm.id'),
                        nullable=False, default=1)
    farm = db.relationship('Farm', backref=db.backref('users', lazy=True), foreign_keys=[farm_id])
    order = db.relationship('Order', backref=db.backref('user_order', lazy=True))


    def json(self):
        return {'id': self.id, 'full_name': self.full_name,
                'Phone_number': self.phone, 'Email': self.email,
                'profile_picture': self.profile_picture, 'Role': self.role,
                'password': self.password, 'location': self.location,
                'Farm_id': self.farm.id,
                'Farm_name': self.farm.farm_name,
                'Farm_Location': self.farm.farm_location
                }

    def add_User(_phone, _full_name, _password, _email, _role):
        '''fuction to add user to the database'''
        new_user = User(phone=_phone, full_name=_full_name,
                        password=_password, email=_email, role=_role,
                        farm_id=1)
        # setting farm id to be 1, which is None for all new users
        # it can be change when they edit their profile
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
            'Farm_id': self.farm.farm_id,
            'Location': self.farm.location
                       }
        return json.dumps(user_object)
