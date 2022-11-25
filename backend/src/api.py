import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from queue import Empty
from turtle import title

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''

#comment the code below on first run
#db_drop_and_create_all()


# ROUTES 

# Endpoint below gets all DRINKS in short format
@app.route('/drinks', methods=['GET'])
def retrieve_drinks():
    req_drinks = Drink.query.all()

    if req_drinks is Empty:
        abort(404)

    drink_short= [drink.short() for drink in req_drinks]

    return jsonify({
        "success": True,
        "drinks": drink_short
    })


# Endpoint to GET drink details 
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def retrieve_drinks_detail(jwt):
    req_drinks_detail = Drink.query.all()

    drink_long_form = [drink.long() for drink in req_drinks_detail]

    return jsonify({
        "success": True,
        "drinks": drink_long_form,
    })



# Endpoint below will add new DRINK
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_new_drink(jwt):
    req_body = request.get_json()

    if req_body is not None:
        new_title = req_body.get('title', None)
        new_recipe = json.dumps(req_body.get('recipe', None))
        new_drink  = Drink(title = new_title, recipe = new_recipe)
        new_drink.insert()
        
        return jsonify({
            "success": True,
            "drinks": new_drink.long()
        }) 
    else:
        abort(404)




'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt, id):
    return json.dumps({
        "success": True
    })

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_specific_drink(jwt, id):
    return json.dumps({
        "success": True
    })

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return json.dumps({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
'''


'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def detect_404_error():
    return json.dumps({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
