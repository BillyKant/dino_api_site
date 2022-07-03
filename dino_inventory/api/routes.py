from flask import Blueprint, request, jsonify
from dino_inventory.helpers import token_required
from dino_inventory.models import db, User, Dino, dino_schema, dinos_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata(current_user_token):
    return{'some':'value'}

# Create Dino Endpoint
@api.route('/dinos', methods = ['POST'])
@token_required
def create_dino(current_user_token):
    name = request.json['name']
    name_meaning = request.json['name_meaning']
    species = request.json['species']
    size = request.json['size']
    lifestyle = request.json['lifestyle']
    era = request.json['era']
    features = request.json['features']
    distribution = request.json['distribution']
    description = request.json['description']
    user_token = current_user_token.token

    print(f"BIG TESTER: {current_user_token.token}")

    dino = Dino(name, name_meaning, species, size, lifestyle, era, features, distribution, description, user_token= user_token)

    db.session.add(dino)
    db.session.commit()

    response = dino_schema.dump(dino)

    return jsonify(response)


# Retrieve all Dino Endpoints
@api.route('/dinos', methods = ['GET'])
@token_required
def get_dinos(current_user_token):
    owner = current_user_token.token
    dinos = Dino.query.filter_by(user_token = owner).all()
    response = dinos_schema.dump(dinos)
    return jsonify(response)


# Retrieve one Dino Endpoints
@api.route('/dinos/<id>', methods = ['GET'])
@token_required
def get_dino(current_user_token, id):
    owner = current_user_token.token
    if owner ==current_user_token.token:
        dino = Dino.query.get(id)
        response = dino_schema.dump(dino)
        return jsonify(response)

    
#Update Dino
@api.route('/dinos/<id>', methods = ['POST', 'PUT'])
@token_required
def update_dino(current_user_token, id):
    dino = Dino.query.get(id)

    dino.name = request.json['name']
    dino.name_meaning = request.json['name_meaning']
    dino.species = request.json['species']
    dino.size = request.json['size']
    dino.lifestyle = request.json['lifestyle']
    dino.era = request.json['era']
    dino.features = request.json['features']
    dino.distribution = request.json['distribution']
    dino.description = request.json['description']
    dino.user_token = current_user_token.token

    db.session.commit()
    response = dino_schema.dump(dino)
    return jsonify(response)

# Delete Dino 
@api.route('/dinos/<id>', methods=['DELETE'])
@token_required
def delete_dino(current_user_token, id):
    dino = Dino.query.get(id)
    db.session.delete(dino)
    db.session.commit()
    response = dino_schema.dump(dino)
    return jsonify(response)

