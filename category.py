'''Module for the Category Class'''
from Product import *


class Category(db.Model):
    '''Category class with table category'''
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def json(self):
        return {'id': self.id, 'Category': self.name
                }

    def add_Category(_name):
        '''fuction to add new category to the database'''
        new_category = Category(name=_name)
        db.session.add(new_category)  # add new category to database
        db.session.commit()   # committing changes

    def getAllCategories():
        '''function to view all categories in the database'''
        return [Category.json(i) for i in Categories.query.all()]

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

    def __repr__(self):
        category_object = {
            'id': self.id,
            'Category': self.name
                          }
        return json.dumps(category_object)
