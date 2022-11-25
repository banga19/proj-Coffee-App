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



# Endpoint below will update DRINKS using the id
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink_list(jwt, id):
    drink_to_update = Drink.query.get(id)
    drink_body = request.get_json()

    if drink_body is not None:
        new_title = drink_body.get('title', None)
        new_recipe = drink_body.get('recipe', None)

        if drink_to_update is None:
            abort(404)
        
        if new_title is not None:
            drink_to_update.title = new_title
        
        if new_recipe is not None:
            new_recipe = json.dumps(new_recipe)
            drink_to_update.recipe = new_recipe

        drink_to_update = Drink.query.all()
        drink_short = [drink.short() for drink in drink_to_update]
        drink_to_update.insert()


        return jsonify({
            "success": True,
            "drinks": drink_to_update
        })
    else:
        abort(404)


#Endpoint below deletes a DRINK according to it's id
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('patch:drinks')
def delete_specific_drink(jwt, id):
    drink_to_delete = Drink.query.get(id)

    if drink_to_delete is None:
        abort (404)
    
    drink_to_delete.delete()

    return jsonify({
        "success": True,
        "deteted": id
    })



# Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "request cannot be processed"
    }), 422

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def detect_404_error():
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Requested resource not cannot be found"
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
