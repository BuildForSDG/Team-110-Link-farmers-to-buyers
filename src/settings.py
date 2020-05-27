from flask import Flask, request, Response, jsonify
from flask_bcrypt import Bcrypt  # hashing password
import json
import jwt
import datetime
from functools import wraps

# creating an instance of the flask app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'cb6586bafe53ec6fba3db37e147c0955'
