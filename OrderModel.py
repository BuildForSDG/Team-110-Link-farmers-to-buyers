'''Module for the Order Class'''
from FarmModel import *


class Order(db.Model):
    '''Order class with table order'''
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    # total_amount = db.Column(db.Integer, unique=False, nullable=False)
    orderItems = db.relationship('OrderItem', backref='orders')

    def json(self):
        return {'id': self.id,
                'user_id': self.user_id,
                'order_date': str(self.order_date),
                # 'total_amount': self.total_amount,
                }

    def add_order(_user_id):
        '''fuction to add user's order to the database'''
        new_order = Order(user_id=_user_id)
        #   total_amount=_total_amount)
        db.session.add(new_order)  # add new order to database
        db.session.commit()  # committing changes

    def getAllUserOrder(_user_id):
        '''function to view all user's orders in the database'''
        user = User.query.filter_by(user_id=_user_id).first()
        # filter by user id
        user_id = user.id  # id of user
        user_name = user.full_name  # fullname of user
        query = db.session.query(User.id, Order.id)
        # display output with user id and order id
        query = query.outerjoin(Order, User.id == Order.user_id)
        query = query.all()
        # leftjoin User table with Order table based on foreign key User.id
        return_value = {"user_id": user_id,
                        "full_name": user_name,
                        "orders": []}
        # output should be json containing user name,
        # user id and all order id belonging to that user
        for i in query:
            if i[0] == _user_id:
                # if the key of the dict is equal to our parameter _user_id
                order = i[1]
                # then the order we need is the value of that key
                return_value["orders"].append(order)
                # while looping through, add the matching product
                # to our order list in the return value dict
        return return_value

    def getAllOrders():
        '''function to view all orders in the database'''
        return [Order.json(i) for i in Order.query.all()]


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
            'order_date': str(self.order_date),
           # 'total_amount': self.total_amount,
                        }
        return json.dumps(order_object)
