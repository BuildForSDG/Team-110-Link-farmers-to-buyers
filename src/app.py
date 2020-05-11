from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy #import SQLAlchemy
from flask_bcrypt import Bcrypt #hashing password
from settings import * 
from FarmerModel import Farmer

import json
import jwt, datetime
from functools import wraps

# creating an instance of the flask app
#app = Flask(__name__)

# creating an instance of the SQLAlchemy class
#db = SQLAlchemy(app)
# Creating an instance of the Bycrypt class
bcrypt = Bcrypt(app)
# configuring the database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
def validFarmerObjectRegistration(bookObject):
    '''Function that validates the data sent to our API'''
    if ("phone_number" in bookObject and "password" in bookObject and "full_name" in bookObject or "email" in bookObject):
        return True
    else:
        return False

# Creating a validation Object for requests sent by client
def validFarmerObjectLogin(bookObject):
    '''Function that validates the data sent to our API'''
    if ("phone_number" in bookObject and "password" in bookObject):
        return True
    else:
        return False


@app.route('/registerFarmer', methods=['GET', 'POST'])
def registerFarmer():
    '''Function to register new farmers'''
    request_data = request.get_json() #getting data from client
    if (validFarmerObjectRegistration(request_data)): #if True
        full_name = str(request_data['full_name'])
        phone = str(request_data['phone_number'])
        email = str(request_data['email'])
        #encrypting password
        password = str(request_data['password'])
        hash_password = bcrypt.generate_password_hash(password).decode('utf-8') 

        #check if someone already registered with that phone number
        phoneExist = Farmer.query.filter_by(phone=phone).first()
        if not phoneExist:
            Farmer.add_Farmer(username, full_name, hash_password) # add new farmer to database
            response = Response("New Farmer added!", 201, mimetype='application/json')
            response.headers['Location'] = "/farmers/" + phone
            return response
        else:
            return Response("Phone number has been used", status=400, mimetype='application/json')

    else:
        invalidFarmerObjectErrorMsg = {
            "error": "Invalid Farmer object passed in request",
            "helpString": "Data passed in similar to this {'full_name' : 'Adonis Chuck', 'phone_number': '070XXXXXXXX', 'email': 'email@email.com','password': 'password'}"
        }
        response = Response(json.dumps(invalidFarmerObjectErrorMsg), status=400, mimetype='application/json')
        return response
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    '''function to log user in and give user token'''
    request_data = request.get_json()
    if (validFarmerObjectLogin(request_data)):
        phone = str(request_data['phone_number'])
        password =  str(request_data['password']) #it needs to be a string, since we will be comparing the value

        #authentication
        farmer = Farmer.query.filter_by(phone=phone).first() #checking if we have login phone number in our database 
        # buyer = Buyer.query.filter_by(phone=phone).first() #checking if we have login phone number in our database     
        if farmer and bcrypt.check_password_hash(farmer.password, password): #if user is in farmer table of database and password of user is equal to the password entered in the form then
            expiration_date = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
            #setting the expiration date of our token. datetime.datetime.utcnow() is the exact time the user will access the route.
            #datetime.timedelta(hours=2) time is set to 2 hours
            #so therefore, the expiration date is 2 hours after token is received
            token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
            # first parameter is a dictionary containing the expiration date
            #second parameter contains the secret key defined earlier
            #third is the algorithm to be used which is HS256 in this case
            return token
        # elif buyer and bcrypt.check_password_hash(buyer.password, password): #if user is in buyer table of database and password of user is equal to the password entered in the form then
        #     expiration_date = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        #     token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        #     return token
        else:
            return Response('Login Unsuccessful. Please check username and password', 401, mimetype='application/json')
    else:
        invalidFarmerObjectErrorMsg = {
            "error": "Invalid Login details passed in request",
            "helpString": "Data passed in similar to this {'phone_number': '070XXXXXXXX', 'password': 'password'}"
        }
        response = Response(json.dumps(invalidFarmerObjectErrorMsg), status=400, mimetype='application/json')
        return response
    
@app.route('\farmer\<phone>', methods=['GET'])
def farmer_profile(phone):
    request_data = request.get_json()
    phone = request_data['phone_number']
    return_value = Farmer.getFarmer(phone) 
    return jsonify(return_value)

   


app.run(debug=True)