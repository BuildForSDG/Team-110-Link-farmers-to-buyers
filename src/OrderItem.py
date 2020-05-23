'''Module for the OrderItem Class'''
from Order import *


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
