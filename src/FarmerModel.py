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

    # defining foreign key and relationship
    farm_id = db.Column(db.Integer, db.ForeignKey('farm.id'),
                        nullable=True)
    farm = db.relationship('Farm', backref=db.backref('users', lazy=True), foreign_keys=[farm_id])

    order = db.relationship('Order', backref='user_order', lazy=True)

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


class Farm(db.Model):
    '''Farm class with table farm'''
    __tablename__ = 'farm'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    farm_name = db.Column(db.String(80))
    farm_location = db.Column(db.String(80))

    def json(self):
        return {'id': self.id, 'Farm name': self.farm_name,
                'Farm Location': self.farm_location,
                'Farmers': self.users.full_name}

    def add_Farm(_farm_name, _farm_location):
        '''fuction to add farm to the database'''
        new_farm = Farm(farm_name=_farm_name, farm_location=_farm_location)
        db.session.add(new_farm)   # add new farm to database
        db.session.commit()   # committing changes

    def getAllFarm():
        '''function to return all farms in the database'''
        return [Farm.json(i) for i in Farm.query.all()]

    def searchFarm(_farm_name):
        '''function to get a farm detail using id as parameter'''
        return [Farm.json(i) for i in Farm.query.filter_by(farm_name=_farm_name).all()]

    def getFarmUser(_farm_id):
        '''function to show all farmers in a farm using farm id as parameter'''
        farm = Farm.query.filter_by(id=_farm_id).first()
        farm_name = farm.farm_name
        farm_location = farm.farm_location
        query = db.session.query(Farm.id, User.full_name)
        query = query.outerjoin(User, Farm.id == User.farm_id).all()
        return_value = {"farm_name": farm_name,
                        "farm_location": farm_location,
                        "farmers": []}
        for i in query:
            if i[0] == _farm_id:
                farmer = i[1]
                return_value["farmers"].append(farmer)
        return return_value

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


class Product(db.Model):
    '''Product class with table product'''
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    # product_name =


class Order(db.Model):
    '''Order class with table order'''
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    total_amount = db.Column(db.Integer, unique=False, nullable=False)
    order_items = db.relationship('OrderItem', backref='orders')

    def json(self):
        return {'id': self.id,
                'user_id': self.user_id,
                'order_date': self.order_date,
                'total_amount': self.total_amount,
                }

    def add_order(_status, _user_id, _order_date, _total_amount):
        '''fuction to add user's order to the database'''
        new_order = Order(status=_status, user_id=_user_id,
                          order_date=_order_date, total_amount=_total_amount)
        db.session.add(new_order)  # add new order to database
        db.session.commit()   # committing changes

    def getAllUserOrder(_user_id):
        '''function to view all user's orders in the database'''
        return Order.json(Order.query.filter_by(user_id=_user_id).all())

    def getOrder(_order_id):
        '''function to view all user's orders in the database'''
        return Order.json(Order.query.filter_by(id=_order_id).first())

    def deleteOrder(_order_id):
        '''function to delete a user's order'''
        is_successful = Order.query.filter_by(id=_order_id).delete()
        db.session.commit()  # commiting the new change to our database
        return bool(is_successful)

    def __repr__(self):
        order_object = {
            'id': self.id,
            'user_id': self.user_id,
            'order_date': self.order_date,
            'total_amount': self.total_amount,
                        }
        return json.dumps(order_object)


class OrderItem(db.Model):
    '''OrderDetails class with table order_details'''
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    quantity = db.Column(db.Integer, unique=False, nullable=False)
    price = db.Column(db.Integer, unique=False, nullable=False)
    total_price = db.Column(db.Integer, unique=False, nullable=False)

    def json(self):
        return {'id': self.id, 'product_id': self.product_id,
                'status': self.status,
                'order_id': self.order_id,
                'quantity': self.quantity,
                'price': self.price,
                'total_price': self.quantity * self.price
                }

    def add_orderItem(_status, _product_id, _order_id, _quantity, _price):
        '''function to add user's order details to the database'''
        new_orderItem = OrderItem(status=_status, order_id=_order_id,
                                  product_id=_product_id,
                                  quantity=_quantity, price=_price,
                                  total_price=_quantity*_price)
        db.session.add(new_orderItem)  # add new order item to database
        db.session.commit()   # committing changes

    def get_orderItems(_order_id):
        '''function to get all orders items in one order'''
        f = OrderItem.query.filter_by(order_id=_order_id).all()
        return OrderItem.json(f)

    def updateStatus(_order_id, _status):
        '''function to update the status of an order'''
        f = OrderItem.query.filter_by(order_id=_order_id).all()
        f.status = _status
        db.session.commit()

    def getOrderItem(_orderItem_id):
        '''function to get order item'''
        f = OrderItem.query.filter_by(id=_orderItem_id).first()
        return OrderItem.json(f)

    def delete_orderItem(_OrderItem_id):
        '''function to delete an order item with orderItemId as parameter'''
        is_successful = OrderItem.query.filter_by(id=_OrderItem_id).delete()
        db.session.commit()  # commiting the new change to our database
        return bool(is_successful)
    
    def __repr__(self):
        order_object = {
        'id': self.id,
        'status': self.status,
        'user_id': self.user_id,
        'total_price': self.total_price
                        }
        return json.dumps(order_object)
