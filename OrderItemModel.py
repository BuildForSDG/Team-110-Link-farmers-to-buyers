'''Module for the OrderItem Class'''
from OrderModel import *


class OrderItem(db.Model):
    '''OrderDetails class with table order_details'''
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    quantity = db.Column(db.Integer, unique=False, nullable=False)
    price = db.Column(db.Integer, unique=False, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)


    def json(self):
        return {'id': self.id, 'product_id': self.product_id,
                'status': self.status,
                'order_id': self.order_id,
                'quantity': self.quantity,
                'price': self.price,
                'total_price': self.quantity * self.price
                }

    def add_orderItem(_status, _product_id, _order_id, _quantity):
        '''function to add user's order details to the database'''
        # retrieve price from product table with product_id
        f = Product.query.filter_by(id=_product_id).first()
        new_orderItem = OrderItem(status=_status, order_id=_order_id,
                                  product_id=_product_id,
                                  quantity=_quantity,
                                  price=f.price,
                                  total_price=_quantity*f.price)
        db.session.add(new_orderItem)  # add new order item to database
        db.session.commit()   # committing changes

    def getOrder(_order_id):
        '''function to get all orders items in one order'''
        f = OrderItem.query.filter_by(order_id=_order_id).all()
        return OrderItem.json(f)

    def updateStatus(_id, _status):
        '''function to update the status of an order'''
        f = OrderItem.query.filter_by(id=_id).first()
        f.status = _status
        db.session.commit()

    def getOrderItem(_orderItem_id):
        '''function to get order item'''
        f = OrderItem.query.filter_by(id=_orderItem_id).first()
        if f is None:
            # if the orderitem id is not in the database
            g = {"Error": "OrderItem ID doesn't exist"}
            return g
        return OrderItem.json(f)

    def delete_orderItem(_OrderItem_id):
        '''function to delete an order item with orderItemId as parameter'''
        is_successful = OrderItem.query.filter_by(id=_OrderItem_id).delete()
        db.session.commit()  # commiting the new change to our database
        return bool(is_successful)

    # function to view all pending orders **************************
    # join order table and order item table and filter by user id and status
    def getPendingOrder(_user_id):
        '''function to get all pending orders'''
        user = User.query.filter_by(id=_user_id).first()
        # filter by user id
        user_id = user.id  # id of user
        user_name = user.full_name  # fullname of user
        query = db.session.query(Order, OrderItem)
        # display output with Order and orderItem
        query = query.outerjoin(OrderItem, Order.id == OrderItem.order_id)
        query = query.all()
        # leftjoin Order table with OrderItem table based on foreign key Order.id
        return_value = {"user_id": user_id,
                        "full_name": user_name,
                        "pending": []}
        # output should be json containing user name, 
        # user id and all order id belonging to that user
        for i in query:
            if i[0] == 1:
                # if the key of the dict is equal to our parameter _user_id
                order = i[1]
                # then the order we need is the value of that key
                return_value["orders"].append(order)
                # while looping through, add the matching product
                # to our order list in the return value dict
        return return_value


    # function to view all finished orders



    def __repr__(self):
        order_object = {
        'id': self.id,
        'status': self.status,
        'total_price': self.total_price
                        }
        return json.dumps(order_object)
