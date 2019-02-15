from flask import jsonify, request, Blueprint, g
# from flask_login import login_required
from flask_httpauth import HTTPBasicAuth
from models import TodoListItem, User

todo_list_api = Blueprint('todo_list_api', __name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(email=username).first()
    if not user or not user.check_password(password):
        return False

    g.user = user
    return True

# TODO: auth and filter by user_id
@todo_list_api.route('/todo/', methods=['GET'])
@auth.login_required
def get_todo_list():
    # items = TodoListItem.query.filter(TodoListItem.user_id = 1)
    items = TodoListItem.query.all()
    return jsonify(results=[i.serialize for i in items]), 200


@todo_list_api.route('/todo/create/', methods=['POST'])
@auth.login_required
def create_todo_list_item():
    request_json = request.get_json()
    
    list_item = TodoListItem(
        text=request_json.get('text'),
        user_id=1
    )
    list_item.save()

    return jsonify(list_item.serialize), 200