'''Module for the Product Class'''
from FarmModel import *


# ##  Define Relationship to Farm, so we can know which farm has which product
class Product(db.Model):
    '''Product class with table product'''
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False) # what (10, 2) means
    stock = db.Column(db.Integer, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)

    # many to one relationship with category table
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
                        nullable=False)
    category = db.relationship('Category',
                               backref=db.backref('product', lazy=True),
                               foreign_keys=[category_id])

    # images of products
    image_1 = db.Column(db.String(150), nullable=False,
                        default='image.jpg')
    image_2 = db.Column(db.String(150), nullable=False,
                        default='image.jpg')
    image_3 = db.Column(db.String(150), nullable=False,
                        default='image.jpg')
    
    
    def json(self):
        return {'id': self.id, 'product_name': self.product_name,
                'price': self.price, 'stock': self.stock,
                'description': self.desc, 'pub_date': self.pub_date,
                'category': self.category.name,
                'image_1': self.image_1,
                'image_2': self.image_2,
                'image_3': self.image_3
                }

    def add_Product(_product_name, _price, _stock, _desc, _category_id,
                    _image_1, _image_2, _image_3):
        '''fuction to add product to the database'''
        new_product = Product(product_name=_product_name,
                              price=_price, stock=_stock, desc=_desc,
                              category_id=_category_id, image_1=_image_1,
                              image_2=_image_2, image_3=_image_3)

        db.session.add(new_product)  # add new product to database
        db.session.commit()   # committing changes

    def getAllProducts():
        '''function to view all products in the database'''
        return [Product.json(i) for i in Product.query.all()]

    def getFarmProduct(_farm_id):
        '''function to get all farm's products using farm id as parameter'''
        return Product.query.filter_by(farm_id=_farm_id).all()

    def editProduct(_id, _product_name, _price, _stock, _desc, _category_id,
                    _image_1, _image_2, _image_3):
        '''Function to edit a product'''
        product_to_update = Product.query.filter_by(id=_id).first()
        product_to_update.product_name = _product_name
        product_to_update.price = _price
        product_to_update.stock = _stock
        product_to_update.desc = _desc
        product_to_update.category_id = _category_id
        product_to_update.image_1 = _image_1
        product_to_update.image_2 = _image_2
        product_to_update.image_3 = _image_3
        db.session.commit()  # commit changes

    def deleteProduct(_id):
        '''function to delete a product'''
        is_successful = Product.query.filter_by(id=_id).delete()
        db.session.commit()  # commiting the new change to our database
        return bool(is_successful)

    def __repr__(self):
        product_object = {
            'id': self.id,
            'product_name': self.product_name,
            'price': self.price,
            'stock': self.stock,
            'description': self.desc,
            'pub_date': self.pub_date,
            'category': self.category.name,
            'image_1': self.image_1,
            'image_2': self.image_2,
            'image_3': self.image_3
            }
        return json.dumps(product_object)
