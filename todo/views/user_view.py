from flask import jsonify, request, Blueprint
from models import User

user_api = Blueprint('user_api', __name__)


@user_api.route('/user/create/', methods=['POST'])
def create_user():
    request_json = request.get_json()

    # password hashing
    user = User(
        email=request_json.get('email')
    )

    user.save()

    return jsonify({'result': 'User created'}), 200