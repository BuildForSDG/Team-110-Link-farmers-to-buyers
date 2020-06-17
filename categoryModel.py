'''Module for the Category Class'''
from ProductModel import *


class Category(db.Model):
    '''Category class with table category'''
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    def json(self):
        return {'id': self.id, 'Category': self.name
                }

    def add_Category(_name):
        '''fuction to add new category to the database'''
        new_category = Category(name=_name)
        db.session.add(new_category)  # add new category to database
        db.session.commit()  # committing changes

    def getAllCategories():
        '''function to view all categories in the database'''
        return [Category.json(i) for i in Category.query.all()]

    def searchCategory(_name):
        '''function to get a category using name as parameter'''
        return [Category.json(i) for i in Category.query.filter_by(name=_name).all()]

    def editCategory(_id, _name):
        '''Function to edit a category'''
        category_to_update = Category.query.filter_by(id=_id).first()
        category_to_update.name = _name
        db.session.commit()  # commit changes

    def deleteCategory(_id):
        '''function to delete a category from database'''
        is_successful = Category.query.filter_by(id=_id).delete()
        db.session.commit()  # commiting the new change to our database
        return bool(is_successful)

    def getCategProducts(_category):
        '''function to show all products in a category
           using category as parameter'''
        categ = Category.query.filter_by(name=_category).first()
        # filter by category name
        categ_name = categ.name  # name of category
        query = db.session.query(Category.name, Product.id)
        # display output with category name and product name
        query = query.outerjoin(Product, Category.id == Product.category_id)
        query = query.all()
        # leftjoin Category with Product table based on foreign key Category.id
        return_value = {"category": categ_name,
                        "products": []}
        # output should be json containing category name
        # and all products id in that category
        for i in query:
            if i[0] == _category:
                # if the key of the dict is equal to our parameter _category
                product = i[1]
                # then the product we need is the value of that key
                return_value["products"].append(product)
                # while looping through, add the matching product
                # to our product list in the return value dict
        return return_value

    def __repr__(self):
        category_object = {
            'id': self.id,
            'Category': self.name
                          }
        return json.dumps(category_object)
