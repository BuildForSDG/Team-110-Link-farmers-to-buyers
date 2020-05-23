'''Module for the Product Class'''


class Product(db.Model):
    '''Product class with table product'''
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    # product_name =