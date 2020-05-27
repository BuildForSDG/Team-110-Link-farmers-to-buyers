'''Module for the Farm Class'''
from UserModel import *


class Farm(db.Model):
    '''Farm class with table farm'''
    __tablename__ = 'farm'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    farm_name = db.Column(db.String(80))
    farm_location = db.Column(db.String(80))

    def json(self):
        return {'id': self.id, 'Farm name': self.farm_name,
                'Farm Location': self.farm_location}

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