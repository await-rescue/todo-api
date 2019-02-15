from flask import jsonify, request, Blueprint, g
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


# TODO: sorting param
@todo_list_api.route('/todo/', methods=['GET'])
@auth.login_required
def get_todo_list():
    # By default we'll hide completed items
    show_completed = request.args.get('show_completed')
    if show_completed in ['true', 'True']:
        items = TodoListItem.query.filter_by(user_id=g.user.id)
    else:
        items = TodoListItem.query.filter_by(user_id=g.user.id, is_completed=False)

    
    return jsonify(results=[i.serialize for i in items]), 200


@todo_list_api.route('/todo/create/', methods=['POST'])
@auth.login_required
def create_todo_list_item():
    request_json = request.get_json()
    if not 'text' in request_json:
        return jsonify({'error': 'Field "text" is required"'}), 400
    
    # TODO: parse date
    list_item = TodoListItem(
        text=request_json.get('text'),
        due_date=request_json.get('due_date'),
        user_id=g.user.id
    )
    list_item.save()

    return jsonify(list_item.serialize), 200

@todo_list_api.route('/todo/<id>/complete/', methods=['PATCH'])
@auth.login_required
def toggle_item_completed(id):
    item = TodoListItem.query.filter_by(user_id=g.user.id, id=id).first()
    if not item:
        return jsonify({'error': '404 not found'}), 404
    
    item.is_completed = not item.is_completed
    item.save()

    return jsonify(results=item.serialize), 200

# TODO: generic update view (modify the model to have an update func)