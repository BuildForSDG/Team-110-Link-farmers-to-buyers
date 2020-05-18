from flask import Flask, request, Response, jsonify
from flask_bcrypt import Bcrypt  # hashing password
from settings import *
from FarmerModel import User, Farm, Order

import json
import jwt
import datetime
from functools import wraps


bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'cb6586bafe53ec6fba3db37e147c0955'

'''
 {
    "full_name" : "Adonis Chuck",
    "phone_number": "070XXXXXXXX",
    "email": "email@email.com",
    "password": "password"
 }
'''

# Creating a validation Object for requests sent by client
def validUserObjectRegistration(UserObject):
    '''Function that validates the Registration data sent to our API'''
    if ("phone_number" in UserObject and "password" in UserObject
            and "full_name" in UserObject and "email" in UserObject
                and "role" in UserObject):
        return True
    else:
        return False


# Creating a validation Object for requests sent by client
def validUserObjectLogin(UserObject):
    '''Function that validates the Login data sent to our API'''
    if ("phone_number" in UserObject and "password" in UserObject):
        return True
    else:
        return False


def validUserObjectDelete(UserObject):
    '''Function that validates the delete user request data sent to our API'''
    if ("phone_number" in UserObject):
        return True
    else:
        return False


def validUserObjectEdit(UserObject):
    '''Function that validates the update user request data sent to our API'''
    if ("phone_number" in UserObject and "password" in UserObject
        and "full_name" in UserObject and "email" in UserObject and
            'profile_picture' in UserObject and 'farm_id' in UserObject):
        return True
    else:
        return False


@app.route('/register', methods=['GET', 'POST'])
def registerUser():
    '''Function to register new users'''
    request_data = request.get_json()  # getting data from client
    if (validUserObjectRegistration(request_data)):  # if True
        full_name = str(request_data['full_name'])
        phone = str(request_data['phone_number'])
        email = str(request_data['email'])
        role = str(request_data['role'])
        #  encrypting password
        password = str(request_data['password'])
        hash_password = bcrypt.generate_password_hash(password).decode('utf-8')

        #  check if someone already registered with that phone number
        phoneExist = User.query.filter_by(phone=phone).first()
        if not phoneExist:
            User.add_User(phone, full_name, hash_password, email, role)
            # add new user to database if phone number isn't used
            response = Response("New User added!", 201,
                                mimetype='application/json')
            response.headers['Location'] = "/user/" + phone
            return response
        else:
            return Response("Phone number has been used", status=400,
                            mimetype='application/json')

    else:
        invalidUserObjectErrorMsg = {
            "error": "Invalid User object passed in request",
            "helpString": {'phone_number': '070XXXXXXXX',
                           'password': 'password'}
                                    }
        response = Response(json.dumps(invalidUserObjectErrorMsg), status=400,
                            mimetype='application/json')
        return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''function to log user in and give user token'''
    request_data = request.get_json()
    if (validUserObjectLogin(request_data)):
        phone = str(request_data['phone_number'])
        password = str(request_data['password'])
        # password needs to be a string, since we will be comparing the value

        # authentication
        user = User.query.filter_by(phone=phone).first()
        # checking if we have login phone number in our database
        if user and bcrypt.check_password_hash(user.password, password):
            # if user is in farmer table of database and password of user
            # is equal to the password entered in the form then
            extra_time = datetime.timedelta(hours=2)
            expiration_date = datetime.datetime.utcnow() + extra_time
            # setting the expiration date of our token will be 2 hrs
            # datetime.timedelta(hours=2) time is set to 2 hours
            exp_dict = {'exp': expiration_date}
            a = 'HS256'  # algorithm
            token = jwt.encode(exp_dict, app.config['SECRET_KEY'], algorithm=a)
            # first parameter is a dictionary containing the expiration date
            # second parameter contains the secret key defined earlier
            # third is the algorithm to be used which is HS256 in this case
            return token
        else:
            return Response('Login Unsuccessful. Check username and password',
                            401, mimetype='application/json')
    else:
        invalidUserObjectErrorMsg = {
            "error": "Invalid Login details passed in request",
            "helpString": {'phone_number': '070XXXXXXXX',
                           'password': 'password'}
                                       }
        response = Response(json.dumps(invalidUserObjectErrorMsg),
                            status=400, mimetype='application/json')
        return response


@app.route('/user', methods=['GET'])
def user_profile(phone):
    '''Function to view a user's profile from phone number'''
    request_data = request.get_json()
    if (validUserObjectDelete(request_data)):
        phone = request_data['phone_number']
        return_value = User.getUser(phone)
        return jsonify(return_value)
    else:
        invalidUserObjectErrorMsg = {
            "error": "Invalid details passed in request",
            "helpString": "Data passed should be {'phone_number': '070XXX'}"
                                    }
        response = Response(json.dumps(invalidUserObjectErrorMsg),
                            status=400, mimetype='application/json')
        return response


@app.route('/farmusers', methods=['GET'])  # test this
def farm_users():
    '''Function to view a farmers in a farm from farm id sent as a request'''
    request_data = request.get_json()
    if (validFarmObjectDelete(request_data)):
        farm_id = int(request_data['farm_id'])
        return_value = Farm.getFarmUser(farm_id)
        return jsonify(return_value)
    else:
        invalidUserObjectErrorMsg = {
            "error": "Invalid details passed in request",
            "helpString": "Data passed should be {'farm_id': 3}"
                                    }
        response = Response(json.dumps(invalidUserObjectErrorMsg),
                            status=400, mimetype='application/json')
        return response


@app.route('/allusers', methods=['GET'])
def all_users():
    '''Function to get all users'''
    return_value = User.getAllUsers()
    return jsonify(return_value)


@app.route('/edituser', methods=['PUT'])
def editUser(phone):
    '''Function to edit user's details with phone number as parameter'''
    request_data = request.get_json()
    if (validUserObjectEdit(request_data)):
        full_name = request_data['full_name']
        phone = request_data['phone_number']
        password = request_data['password']
        hash_password = bcrypt.generate_password_hash(password).decode('utf-8')
        profile_picture = request_data['profile_picture']
        farm_id = int(request_data['farm_id'])
        email = request_data['email']
        User.editUser(phone, full_name, hash_password, profile_picture,
                      farm_id, email)
        return Response("Profile Successfully Updated", status=400,
                        mimetype='application/json')
    else:
        invalidUserObjectErrorMsg = {
            "error": "Invalid Login details passed in request",
            "helpString": {'phone_number': '070XX', 'password': 'password',
                           'full_name': 'XYZ',
                           'profile_picture': 'default.jpg',
                           'farm_id': 5, 'email': 'X@gmail.com'
                           }
                                    }
        response = Response(json.dumps(invalidUserObjectErrorMsg),
                            status=400, mimetype='application/json')
        return response


@app.route('/deleteuser', methods=['DELETE'])
def delete_user(phone):
    '''Function to delete user's profile with phone number as parameter'''
    request_data = request.get_json()
    if (validUserObjectDelete(request_data)):
        phone = request_data['phone_number']
        if (User.deleteUser(phone)):
            response = Response("Account Deleted", status=204)
            return response

        invalidUserObjectErrorMsg = {
            "error": "User with the phone no that was provided was not found"
                                    }
        response = Response(json.dumps(invalidUserObjectErrorMsg), status=404,
                            mimetype='application/json')
        return response
    else:
        invalidUserObjectErrorMsg = {
            "error": "Invalid details passed in request",
            "helpString": "Data passed should be {'phone_number': '070XXX'}"
                                    }


# ---------------------------------------------------
# Farm Section
def validFarmObjectRegistration(FarmObject):
    '''Function that validates the Farm registration data sent to our API'''
    if ("farm_name" in FarmObject and "farm_location" in FarmObject):
        return True
    else:
        return False


def validFarmObjectDelete(FarmObject):
    '''Function that checks the delete & get farm request data sent'''
    if ("farm_id" in FarmObject):
        return True
    else:
        return False


def validFarmObjectEdit(FarmObject):
    '''Function that validates the Farm update data sent to our API'''
    if ("farm_name" in FarmObject and "farm_location" in FarmObject
            and "farm_id" in FarmObject):
        return True
    else:
        return False


def validFarmObjectFarmSearch(FarmObject):
    '''Function that validates the Farm name search data sent to our API'''
    if ("farm_name" in FarmObject):
        return True
    else:
        return False


@app.route('/addfarm', methods=['GET', 'POST'])
def addFarm():
    '''Function to add new farm'''
    request_data = request.get_json()  # getting data from client
    if (validFarmObjectRegistration(request_data)):  # if True
        farm_name = str(request_data['farm_name'])
        farm_location = str(request_data['farm_location'])

        #  check if someone already registered with that phone number
        farmExist = Farm.query.filter_by(farm_name=farm_name)
        farmExist = farmExist.filter_by(farm_location=farm_location).first()
        if not farmExist:  # if farm doesn't exist
            Farm.add_Farm(farm_name, farm_location)
            # add new farm to database if it doesn't exist
            response = Response("New Farm added!", 201,
                                mimetype='application/json')
            # get id of new farm
            f = Farm.query.filter_by(farm_name=farm_name)
            f = f.filter_by(farm_location=farm_location).first()
            response.headers['Location'] = "/farm/" + str(f.id)
            return response
        else:
            return Response("Farm Exists Already", status=400,
                            mimetype='application/json')

    else:
        invalidFarmObjectErrorMsg = {
            "error": "Invalid Farm object passed in request",
            "helpString": {'farm_name': 'XX',
                           'farm_location': 'Lagos'}
                                    }
        response = Response(json.dumps(invalidFarmObjectErrorMsg), status=400,
                            mimetype='application/json')
        return response


@app.route('/allfarms', methods=['GET'])
def all_farms():
    '''Function to get all farms'''
    return_value = Farm.getAllFarm()
    return jsonify(return_value)


@app.route('/farm/<int:farm_id>', methods=['GET'])
def farm_detail(farm_id):
    '''Function to view a farm detail from farm_id'''
    return_value = Farm.getFarm(farm_id)
    return jsonify(return_value)


@app.route('/searchfarm', methods=['GET'])
def farm_search():
    '''Function to view a farm detail from farm_id'''
    request_data = request.get_json()
    if (validFarmObjectFarmSearch(request_data)):
        farm_name = str(request_data['farm_name'])
        return_value = Farm.searchFarm(farm_name)
        return jsonify(return_value)
    else:
        invalidFarmObjectErrorMsg = {
            "error": "Invalid Farm details passed in request",
            "helpString": {'farm_name': 'XX'}
                                    }
        response = Response(json.dumps(invalidFarmObjectErrorMsg),
                            status=400, mimetype='application/json')
        return response


@app.route('/editfarm', methods=['PUT'])
def edit_user():
    '''Function to edit a farm's details with farm_id as parameter'''
    request_data = request.get_json()
    if (validFarmObjectEdit(request_data)):
        farm_id = int(request_data['farm_id'])
        farm_name = str(request_data['farm_name'])
        farm_location = str(request_data['farm_location'])
        Farm.editFarm(farm_id, farm_name, farm_location)
        return Response("Farm Successfully Updated", status=400,
                        mimetype='application/json')
    else:
        invalidFarmObjectErrorMsg = {
            "error": "Invalid Farm details passed in request",
            "helpString": {'farm_id': '4', 'farm_name': 'XX',
                           'farm_location': 'Lagos'}
                                    }
        response = Response(json.dumps(invalidFarmObjectErrorMsg),
                            status=400, mimetype='application/json')
        return response


@app.route('/deletefarm', methods=['DELETE'])
def delete_farm():
    '''Function to delete a farm using farm_id'''
    request_data = request.get_json()
    if (validFarmObjectDelete(request_data)):
        farm_id = int(request_data['farm_id'])
        if (Farm.deleteFarm(farm_id)):
            response = Response("Farm Deleted", status=204)
            return response

        invalidFarmObjectErrorMsg = {
            "error": "Farm with the farm_id that was provided was not found"
                                    }
        response = Response(json.dumps(invalidFarmObjectErrorMsg), status=404,
                            mimetype='application/json')
        return response
    else:
        invalidFarmObjectErrorMsg = {
            "error": "Invalid details passed in request",
            "helpString": "Data passed should be {'farm_id': 4}"
                                    }
        response = Response(json.dumps(invalidFarmObjectErrorMsg), status=400,
                            mimetype='application/json')
        return response


if __name__ == "__main__":
    app.run(debug=True)

# app.run(debug=True)
