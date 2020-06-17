'''All routes for user Table'''

from flask import Response, request
from validate_email import validate_email
from settings import *  # importing the setting module
from OrderItemModel import *


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


def space(text):
    '''function to check for spaces in text'''
    for i in text:
        if i.isspace():
            return True
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

        # validate phone number
        if phone.isnumeric() is False:
            return Response("Phone number is invalid", status=400,
                            mimetype='application/json')

        is_valid = validate_email(email)
        if is_valid is False:
            return Response("Invalid email", status=400,
                            mimetype='application/json')
        # validating email
        if space(email) is True:
            return Response("Please remove whitespace in email", status=400,
                            mimetype='application/json')

        # validating password
        if space(password) is True:
            return Response("Please remove whitespace in password", status=400,
                            mimetype='application/json')

        # validating user role
        if (role != "Buyer" and role != "Farmer"):
            # if logic is 1 (True) then the invalid role will be returned
            # else logic is 0 (False), the invalid role won't be returned
            invalidRoleObjectErrorMsg = {
                "error": "Invalid Role object passed in request",
                "helpString": "status value should be 'Buyer' or 'Farmer'"}

            response = Response(json.dumps(invalidRoleObjectErrorMsg),
                                status=400,
                                mimetype='application/json')
            return response

        hash_password = bcrypt.generate_password_hash(password).decode('utf-8')
        # check if someone already registered with that phone number
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
            "helpString": {'full_name': 'your_name',
                           'phone_number': '070XXXXXXXX',
                           'password': 'password',
                           'email': 'xyz@email.com',
                           'role': 'Buyer'}
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
def user_profile():
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
    '''Function to view farmers in a farm from farm id sent as a request'''
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
def editUser():
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
        return Response("Profile Successfully Updated", status=201,
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
def delete_user():
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

# Farm ********************************************

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

@app.route('/farmproducts', methods=['GET', 'POST'])
def farm_products():
    '''Function to view a farm detail from farm_id'''
    request_data = request.get_json()  # get data from client
    if (validFarmObjectDelete(request_data)):  # if true
        farm_id = int(request_data['farm_id'])
        return_value = Farm.getFarmProducts(farm_id)
        response = Response(json.dumps(return_value),
                            status=201, mimetype='application/json')
        return response
    else:
        invalidFarmObjectErrorMsg = {
            "error": "Invalid Farm details passed in request",
            "helpString": {'farm_id': 5}
                                    }
        response = Response(json.dumps(invalidFarmObjectErrorMsg),
                            status=400, mimetype='application/json')
        return response


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
    '''Function to edit a farm's details'''
    request_data = request.get_json()
    if (validFarmObjectEdit(request_data)):
        farm_id = int(request_data['farm_id'])
        farm_name = str(request_data['farm_name'])
        farm_location = str(request_data['farm_location'])
        Farm.editFarm(farm_id, farm_name, farm_location)
        return Response("Farm Successfully Updated", status=201,
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

# Category -----------------------------------------
def validCategObjectAdd(CategObject):
    '''Function that validates the new category data sent to our API'''
    if ("category" in CategObject):
        return True
    else:
        return False


def validCategObjectDelete(CategObject):
    '''Function that validates the deletes & get category request data sent'''
    if ("category_id" in CategObject):
        return True
    else:
        return False


def validCategObjectEdit(CategObject):
    '''Function that validates the category update data sent to our API'''
    if ("category_id" in CategObject and "category" in CategObject):
        return True
    else:
        return False


def validCategObjectSearch(CategObject):
    '''Function that validates the Category search data sent to our API'''
    if ("category" in CategObject):
        return True
    else:
        return False


@app.route('/addcateg', methods=['GET', 'POST'])
def addCateg():
    '''Function to add new category'''
    request_data = request.get_json()  # getting data from client
    if (validCategObjectAdd(request_data)):  # if True
        category = str(request_data['category'])

        #  check if someone category already exist
        CategExist = Category.query.filter_by(name=category).first()
        if not CategExist:  # if category doesn't exist
            Category.add_Category(category)
            # add new category to database if it doesn't exist
            response = Response("New Category added!", 201,
                                mimetype='application/json')
            return response
        else:
            return Response("Category Already Exists", status=400,
                            mimetype='application/json')

    else:
        invalidCategObjectErrorMsg = {
            "error": "Invalid Category object passed in request",
            "helpString": {'category': 'XX'}
                                    }
        response = Response(json.dumps(invalidCategObjectErrorMsg), status=400,
                            mimetype='application/json')
        return response


@app.route('/allcateg', methods=['GET'])
def all_category():
    '''Function to get all categories'''
    return_value = Category.getAllCategories()
    return jsonify(return_value)


@app.route('/searchcateg', methods=['GET'])
def categ_search():
    '''Function to search for a category'''
    request_data = request.get_json()
    if (validCategObjectSearch(request_data)):
        category = str(request_data['category'])
        return_value = Category.searchCategory(category)
        return jsonify(return_value)
    else:
        invalidCategObjectErrorMsg = {
            "error": "Invalid Category details passed in request",
            "helpString": {'category': 'XX'}
                                    }
        response = Response(json.dumps(invalidCategObjectErrorMsg),
                            status=400, mimetype='application/json')
        return response
        
@app.route('/categproducts', methods=['GET', 'POST'])
def categ_products():
    '''Function to view all products in a category'''
    request_data = request.get_json()  # get data from client
    if (validCategObjectSearch(request_data)):  # if true
        category = str(request_data['category'])
        return_value = Category.getCategProducts(category)
        response = Response(json.dumps(return_value),
                            status=201, mimetype='application/json')
        return response
    else:
        invalidCategObjectErrorMsg = {
            "error": "Invalid Farm details passed in request",
            "helpString": {'category': 'Livestock'}
                                    }
        response = Response(json.dumps(invalidCategObjectErrorMsg),
                            status=400, mimetype='application/json')
        return response



@app.route('/editcateg', methods=['PUT'])
def edit_category():
    '''Function to edit a category'''
    request_data = request.get_json()
    if (validCategObjectEdit(request_data)):
        category_id = int(request_data['category_id'])
        category = str(request_data['category'])
        Category.editCategory(category_id, category)
        return Response("Category Successfully Updated", status=201,
                        mimetype='application/json')
    else:
        invalidCategObjectErrorMsg = {
            "error": "Invalid Farm details passed in request",
            "helpString": {'category_id': '4', 'category': 'XX'}
                                    }
        response = Response(json.dumps(invalidCategObjectErrorMsg),
                            status=400, mimetype='application/json')
        return response


@app.route('/deletecateg', methods=['DELETE'])
def delete_category():
    '''Function to delete a category'''
    request_data = request.get_json()
    if (validCategObjectDelete(request_data)):
        category_id = int(request_data['category_id'])
        if (Category.deleteCategory(category_id)):
            response = Response("Category Deleted", status=204)
            return response

        invalidCategObjectErrorMsg = {
            "error": "Category with the category_id that was provided was not found"
                                    }
        response = Response(json.dumps(invalidCategObjectErrorMsg), status=404,
                            mimetype='application/json')
        return response
    else:
        invalidCategObjectErrorMsg = {
            "error": "Invalid details passed in request",
            "helpString": "Data passed should be {'category_id': 4}"
                                    }
        response = Response(json.dumps(invalidCategObjectErrorMsg), status=400,
                            mimetype='application/json')
        return response

# Product ***********************************************

# Creating a validation Object for requests sent by client
def validProductObjectAdd(ProductObject):
    '''Function that validates the product addition data sent to our API'''
    if ("product_name" in ProductObject and "price" in ProductObject
            and "stock" in ProductObject and "description" in ProductObject
                and "category_id" in ProductObject
                    and "farm_id" in ProductObject
                        and "image_1" in ProductObject
                            and "image_2" in ProductObject
                            and "image_3" in ProductObject):
        return True
    else:
        return False


def validProductObjectDelete(ProductObject):
    '''Function that validates the delete and get product request
       data sent to our API'''
    if ("product_id" in ProductObject):
        return True
    else:
        return False


def validProductObjectEdit(ProductObject):
    '''Function that validates the update product request
       data sent to our API'''
    if ("product_name" in ProductObject and "price" in ProductObject
            and "stock" in ProductObject and "description" in ProductObject
                and "category_id" in ProductObject
                        and "image_1" in ProductObject
                            and "image_2" in ProductObject
                                and "image_3" in ProductObject
                                    and "product_id" in ProductObject):
        return True
    else:
        return False


@app.route('/addproduct', methods=['POST'])
def addProduct():
    '''Function to add new products'''
    request_data = request.get_json()  # getting data from client
    if (validProductObjectAdd(request_data)):  # if True
        product_name = str(request_data['product_name'])
        price = int(request_data['price'])
        stock = int(request_data['stock'])
        desc = str(request_data['description'])
        category_id = int(request_data['category_id'])
        farm_id = int(request_data['farm_id'])
        image_1 = str(request_data['image_1'])
        image_2 = str(request_data['image_2'])
        image_3 = str(request_data['image_3'])
        Product.add_Product(product_name, price, stock, desc, category_id,
                            farm_id, image_1, image_2, image_3)
        response = Response("New Product added!", 201,
                            mimetype='application/json')
        return response
    else:
        invalidProductObjectErrorMsg = {
            "error": "Invalid Product object passed in request",
            "helpString": {'product_name': 'product_name',
                           'price': 250, 'stock': 11,
                           'description': 'this is a product',
                           'category_id': 2,
                           'farm_id': 3,
                           'image_1': 'image_1',
                           'image_2': 'image_2',
                           'image_3': 'image_3'}
                                    }
        response = Response(json.dumps(invalidProductObjectErrorMsg),
                            status=400,
                            mimetype='application/json')
        return response


@app.route('/product/<int:_id>', methods=['GET'])
def view_product(_id):
    '''Function to view a product from product id'''
    return_value = Product.getProduct(_id)
    return jsonify(return_value)


@app.route('/allproducts', methods=['GET'])
def all_products():
    '''Function to get all products'''
    return_value = Product.getAllProducts()
    response = Response(json.dumps(return_value),
                        status=201, mimetype='application/json')
    return response


@app.route('/editproduct', methods=['PUT'])
def editProduct():
    '''Function to edit product details with product id as parameter'''
    request_data = request.get_json()
    if (validProductObjectEdit(request_data)):
        product_id = int(request_data['product_id'])
        product_name = str(request_data['product_name'])
        price = int(request_data['price'])
        stock = int(request_data['stock'])
        desc = str(request_data['description'])
        category_id = int(request_data['category_id'])
        image_1 = str(request_data['image_1'])
        image_2 = str(request_data['image_2'])
        image_3 = str(request_data['image_3'])

        Product.editProduct(product_id, product_name, price, stock, desc, category_id,
                            image_1, image_2, image_3)
        return Response("Product Successfully Updated", status=201,
                        mimetype='application/json')
    else:
        invalidProductObjectErrorMsg = {
            "error": "Invalid Product object passed in request",
            "helpString": {'product_id': 1,
                           'product_name': 'product_name',
                           'price': 250, 'stock': 11,
                           'description': 'this is a product',
                           'category_id': 2,
                           'farm_id': 3,
                           'image_1': 'image_1',
                           'image_2': 'image_2',
                           'image_3': 'image_3'}
                                    }
        response = Response(json.dumps(invalidProductObjectErrorMsg),
                            status=400,
                            mimetype='application/json')
        return response


@app.route('/deleteproduct', methods=['DELETE'])
def delete_product():
    '''Function to delete product with product id as parameter'''
    request_data = request.get_json()
    if (validProductObjectDelete(request_data)):
        product_id = request_data['product_id']
        if (Product.deleteProduct(product_id)):
            response = Response(json.dumps("Product Deleted"), status=204)
            return response

        invalidProductObjectErrorMsg = {
            "error": "Product with the product id that was provided was not found"
                                    }
        response = Response(json.dumps(invalidProductObjectErrorMsg), status=404,
                            mimetype='application/json')
        return response
    else:
        invalidProductObjectErrorMsg = {
            "error": "Invalid details passed in request",
            "helpString": "Data passed should be {'product_id': 3}"
                                    }
        response = Response(json.dumps(invalidProductObjectErrorMsg), status=404,
                            mimetype='application/json')
        return response


# ORDER *********************

def validOrderObjectAdd(OrderObject):
    '''Function that validates the new order data sent to our API'''
    if ("user_id" in OrderObject):
        return True
    else:
        return False


def validOrderObjectDelete(OrderObject):
    '''Function that validates the deletes & get order request data sent'''
    if ("order_id" in OrderObject):
        return True
    else:
        return False


@app.route('/addorder', methods=['GET', 'POST'])
def addOrder():
    '''Function to add new order'''
    request_data = request.get_json()  # getting data from client
    if (validOrderObjectAdd(request_data)):  # if True
        user_id = int(request_data['user_id'])
        Order.add_order(user_id)
        response = Response("New Order Created!", 201,
                            mimetype='application/json')
        return response
    else:
        invalidOrderObjectErrorMsg = {
            "error": "Invalid Order object passed in request",
            "helpString": {'user_id': 4}
                                    }
        response = Response(json.dumps(invalidOrderObjectErrorMsg), status=400,
                            mimetype='application/json')
        return response


@app.route('/allorders', methods=['GET'])
def all_orders():
    '''Function to get all orders'''
    return_value = Order.getAllOrders()
    return jsonify(return_value)

@app.route('/order', methods=['GET'])
def user_order():
    '''Function to view a user's orders from user id'''
    request_data = request.get_json()
    if (validOrderObjectAdd(request_data)):
        user_id = request_data['user_id']
        return_value = Order.getAllUserOrder(user_id)
        response = Response(json.dumps(return_value),
                            status=200, mimetype='application/json')
        return response

    else:
        invalidOrderObjectErrorMsg = {
            "error": "Invalid details passed in request",
            "helpString": "Data passed should be {'user_id': 7}"
                                    }
        response = Response(json.dumps(invalidOrderObjectErrorMsg),
                            status=400, mimetype='application/json')
        return response


@app.route('/deleteorder', methods=['DELETE'])
def delete_order():
    ''''Function to delete an order'''
    request_data = request.get_json()
    if (validOrderObjectDelete(request_data)):
        order_id = int(request_data['order_id'])
        if (Order.deleteOrder(order_id)):
            message = "Order Deleted"
            response = Response(json.dumps(message), status=204,
                            mimetype='application/json')
            return response

        invalidOrderObjectErrorMsg = {
            "error": "Order with the order_id that was provided was not found"
                                    }
        response = Response(json.dumps(invalidOrderObjectErrorMsg), status=404,
                            mimetype='application/json')
        return response
    else:
        invalidOrderObjectErrorMsg = {
            "error": "Invalid details passed in request",
            "helpString": "Data passed should be {'order_id': 4}"
                                    }
        response = Response(json.dumps(invalidOrderObjectErrorMsg), status=400,
                            mimetype='application/json')
        return response


# ORDER ITEMS *********************************

# Creating a validation Object for requests sent by client
def validOrderItemObjectAdd(OIObject):
    '''Function that validates the orderItem addition data sent to our API'''
    if ("product_id" in OIObject
            and "status" in OIObject and "quantity" in OIObject
                and "order_id" in OIObject
                    ):
        return True
    else:
        return False


def validOrderItemObjectDelete(OIObject):
    '''Function that validates the delete and get orderItem request
       data sent to our API'''
    if ("orderItem_id" in OIObject):
        return True
    else:
        return False


def validOrderItemObjectEdit(OIObject):
    '''Function that validates the update orderItem status request
       data sent to our API'''
    if ("status" in OIObject and "orderItem_id"):
        return True
    else:
        return False


@app.route('/orderitem', methods=['POST'])
def addOrderItem():
    '''Function to add new products'''
    request_data = request.get_json()  # getting data from client
    if (validOrderItemObjectAdd(request_data)):  # if True
        product_id = int(request_data['product_id'])
        quantity = int(request_data['quantity'])
        status = str(request_data['status'])
        order_id = int(request_data['order_id'])
        if status != "Pending" and status != "Finished":
            invalidOrderItemObjectErrorMsg = {
                "error": "Invalid Status object passed in request",
                "helpString": "status value should be 'Pending' or 'Finished'"}

            response = Response(json.dumps(invalidOrderItemObjectErrorMsg),
                                status=400,
                                mimetype='application/json')
            return response
        OrderItem.add_orderItem(_status=status, _product_id=product_id,
                                _order_id=order_id, _quantity=quantity)
        response = Response("New OrderItem added!", 201,
                            mimetype='application/json')
        return response
    else:
        invalidOrderItemObjectErrorMsg = {
            "error": "Invalid OrderItem object passed in request",
            "helpString": {"product_id": 1,
                           "status": "Pending",
                           "quantity": 4,
                           "order_id": 2}
                                    }
        response = Response(json.dumps(invalidOrderItemObjectErrorMsg),
                            status=400,
                            mimetype='application/json')
        return response


@app.route('/orderitem/<int:_id>', methods=['GET'])
def view_orderItem(_id):
    '''Function to view an orderItem from orderItem id'''
    return_value = OrderItem.getOrderItem(_id)
    return jsonify(return_value)


@app.route('/orderitem', methods=['PATCH'])
def editOrderItemStatus():
    '''Function to edit status details with orderItem id as parameter'''
    request_data = request.get_json()
    if (validOrderItemObjectEdit(request_data)):
        orderItem_id = int(request_data['orderItem_id'])
        status = str(request_data['status'])
        if status != "Pending" and status != "Finished":
            invalidOrderItemObjectErrorMsg = {
                "error": "Invalid Status object passed in request",
                "helpString": "status value should be 'Pending' or 'Finished'"}

            response = Response(json.dumps(invalidOrderItemObjectErrorMsg),
                                status=400,
                                mimetype='application/json')
            return response

        OrderItem.updateStatus(orderItem_id, status)
        return Response("Order Item Successfully Updated", status=201,
                        mimetype='application/json')
    else:
        invalidOrderItemObjectErrorMsg = {
            "error": "Invalid Order Item object passed in request",
            "helpString": {'orderItem_id': 1,
                           'status': 'Finished'
                          }
                                            }
        response = Response(json.dumps(invalidOrderItemObjectErrorMsg),
                            status=400,
                            mimetype='application/json')
        return response


@app.route('/orderitem', methods=['DELETE'])
def delete_orderItem():
    '''Function to delete orderItem with orderItem id as parameter'''
    request_data = request.get_json()
    if (validOrderItemObjectDelete(request_data)):
        orderItem_id = request_data['orderItem_id']
        if (OrderItem.delete_orderItem(orderItem_id)):
            response = Response(json.dumps("Order Item Deleted"), status=204)
            return response

        invalidOrderItemObjectErrorMsg = {
            "error": "Order Item with the order item id that was provided was not found"
                                    }
        response = Response(json.dumps(invalidOrderItemObjectErrorMsg), status=404,
                            mimetype='application/json')
        return response
    else:
        invalidOrderItemObjectErrorMsg= {
            "error": "Invalid details passed in request",
            "helpString": "Data passed should be {'orderItem_id': 3}"
                                    }
        response = Response(json.dumps(invalidOrderItemObjectErrorMsg), status=404,
                            mimetype='application/json')
        return response

# view all pending orders with user id


# view all finished orders with user id
