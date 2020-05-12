from flask import Flask, request, Response, jsonify
from flask_bcrypt import Bcrypt  # hashing password
from settings import app
from FarmerModel import User, Farm, Order

import json
import jwt, datetime
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
        and "full_name" in UserObject or "email" in UserObject):
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


@app.route('/register', methods=['GET', 'POST'])
def registerFarmer():
    '''Function to register new users'''
    request_data = request.get_json()  # getting data from client
    if (validUserObjectRegistration(request_data)):  # if True
        full_name = str(request_data['full_name'])
        phone = str(request_data['phone_number'])
        email = str(request_data['email'])
        #  encrypting password
        password = str(request_data['password'])
        hash_password = bcrypt.generate_password_hash(password).decode('utf-8')

        #  check if someone already registered with that phone number
        phoneExist = User.query.filter_by(phone=phone).first()
        if not phoneExist:
            User.add_User(phone, full_name, hash_password, email)
            # add new user to database if phone number isn't used
            response = Response("New Farmer added!", 201,
                                mimetype='application/json')
            response.headers['Location'] = "/user/" + phone
            return response
        else:
            return Response("Phone number has been used", status=400,
                            mimetype='application/json')

    else:
        invalidUserObjectErrorMsg = {
            "error": "Invalid Farmer object passed in request",
            "helpString": "Data passed in similar to this {'phone_number': '070XXXXXXXX', 'password': 'password'}"
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
            token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
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
            "helpString": "Data passed in similar to this {'phone_number': '070XXXXXXXX', 'password': 'password'}"
                                       }
        response = Response(json.dumps(invalidUserObjectErrorMsg),
                            status=400, mimetype='application/json')
        return response


@app.route('\user\<phone>', methods=['GET'])
def user_profile(phone):
    '''Function to get user's details from phone number'''
    request_data = request.get_json()
    phone = request_data['phone_number']
    return_value = User.getUser(phone)
    return jsonify(return_value)


@app.route('\allusers', methods=['GET'])
def all_users():
    '''Function to get all users'''
    return_value = User.getAllUsers()
    return jsonify(return_value)


@app.route('\edituser\<phone>', methods=['PUT'])
def edit_user(phone):
    '''Function to edit user's details with phone number as parameter'''
    request_data = request.get_json()
    full_name = request_data['full_name']
    phone = request_data['phone_number']
    password = request_data['password']
    hash_password = bcrypt.generate_password_hash(password).decode('utf-8')
    profile_picture = request_data['profile_picture']
    farm_id = request_data['farm_id']
    email = request_data['email']
    User.editUser(phone, full_name, password, profile_picture, farm_id, email)
    return Response("Profile Successfully Updated", status=400,
                    mimetype='application/json')


@app.route('\deleteuser\<phone>', methods=['DELETE'])
def delete_user(phone):
    '''Function to delete user's profile with phone number as parameter'''
    request_data = request.get_json()
    phone = request_data['phone_number']
    if (User.deleteUser(phone)):
        response = Response("Account Deleted", status=204)
        return response

    invalidUserObjectErrorMsg = {
        "error": "User with the phone number that was provided was not found"
    }
    response = Response(json.dumps(invalidUserObjectErrorMsg), status=404,
                        mimetype='application/json')
    return response


if __name__ == "__main__":
    app.run(debug=True)

# app.run(debug=True)
