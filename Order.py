'''Module for the Order Class'''
from FarmModel import *


class Order(db.Model):
    '''Order class with table order'''
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    total_amount = db.Column(db.Integer, unique=False, nullable=False)
    orderItems = db.relationship('OrderItem', backref='orders')
    
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
