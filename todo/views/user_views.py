from flask import jsonify, request, Blueprint

from models import User

user_api = Blueprint('user_api', __name__)


@user_api.route('/user/create/', methods=['POST'])
def create_user():
    request_json = request.get_json()

    if not 'email' in request_json or not 'password' in request_json:
        return jsonify({'error': 'Fields "email" and "password are required"'}), 400

    try:
        User(
            email=request_json.get('email'),
            password=request.json.get('password')
        ).save()
    except:
        return jsonify({'error': 'Failed to create user'}), 500

    return jsonify({'result': 'User created'}), 201