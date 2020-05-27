from flask import Flask, request, Response, jsonify
from flask_bcrypt import Bcrypt  # hashing password
import json
import jwt
import datetime
from functools import wraps

# creating an instance of the flask app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://mvymvuyiuqqsgy:15e21d859f06631f0dc13638bec9e93bb16758f5378b741445ad3c26079442ff@ec2-18-232-143-90.compute-1.amazonaws.com:5432/d117uq6mcbct16'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'cb6586bafe53ec6fba3db37e147c0955'
