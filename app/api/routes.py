from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Coffee, coffee_schema, coffees_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/testdata')
def getdata():
    return {'test': 'good'}

@api.route('/drinks', methods = ['POST'])
@token_required
def add_drink(current_user_token):
    name = request.json['name']
    drink_type = request.json['drink_type']
    credit = request.json['credit']
    photo = request.json['photo']
    desc = request.json['desc']
    directions = request.json['directions']
    ingredients = request.json['ingredients']
    user_token = current_user_token.token

    print(f'TEST: {current_user_token}')

    drink = Coffee(name, drink_type, credit, photo, desc, directions, ingredients, user_token = user_token)

    db.session.add(drink)
    db.session.commit()

    response = coffee_schema.dump(drink)
    return jsonify(response)

@api.route('/drinks', methods = ['GET'])
@token_required
def get_drinks(current_user_token):
    a_user = current_user_token.token
    drinks = Coffee.query.filter_by(user_token = a_user).all()
    response = coffees_schema.dump(drinks)
    return jsonify(response)

@api.route('/drinks/<id>', methods = ['GET'])
@token_required
def get_drink(current_user_token, id):
    drink = Coffee.query.get(id)
    response = coffee_schema.dump(drink)
    return jsonify(response)

@api.route('/drinks/<id>', methods = ['POST', 'PUT'])
@token_required
def update_drink(current_user_token, id):
    drink = Coffee.query.get(id)

    if 'name' in request.json:
        drink.name = request.json['name']
    if 'drink_type' in request.json:
        drink.drink_type = request.json['drink_type']
    if 'credit' in request.json:
        drink.credit = request.json['credit']
    if 'photo' in request.json:
        drink.photo = request.json['photo']
    if 'desc' in request.json:
        drink.desc = request.json['desc']
    if 'directions' in request.json:
        drink.directions = request.json['directions']
    if 'ingredients' in request.json:
        drink.ingredients = request.json['ingredients']

    db.session.commit()
    response = coffee_schema.dump(drink)
    return jsonify(response)

@api.route('/drinks/<id>', methods = ['DELETE'])
@token_required
def delete_drink(current_user_token, id):
    drink = Coffee.query.get(id)
    db.session.delete(drink)
    db.session.commit()
    response = coffee_schema.dump(drink)
    return jsonify(response)