from dateutil import parser

from flask import jsonify, request, Blueprint, g
from flask_httpauth import HTTPBasicAuth
from models import TodoListItem, User
from db import db_session

todo_list_api = Blueprint('todo_list_api', __name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(email=username).first()
    if not user or not user.check_password(password):
        return False

    g.user = user
    return True


@todo_list_api.route('/todo/', methods=['GET'])
@auth.login_required
def get_todo_list():
    # By default we'll hide completed items
    show_completed = request.args.get('show_completed')
    if show_completed in ['true', 'True']:
        items = TodoListItem.query.filter_by(user_id=g.user.id)
    else:
        items = TodoListItem.query.filter_by(user_id=g.user.id, is_completed=False)

    sort = request.args.get('sort')
    if sort:
        items = items.order_by(TodoListItem.due_date)

    return jsonify(results=[i.serialize for i in items]), 200


@todo_list_api.route('/todo/create/', methods=['POST'])
@auth.login_required
def create_todo_list_item():
    request_json = request.get_json()
    if not 'text' in request_json:
        return jsonify({'error': 'Field "text" is required"'}), 400
    
    due_date = None
    if request_json.get('due_date'):
        try:
            due_date = parser.parse(request_json.get('due_date'))
        except ValueError:
            return jsonify({'error': 'invalid date'}), 400

    list_item = TodoListItem(
        text=request_json.get('text'),
        due_date=due_date,
        user_id=g.user.id
    )
    list_item.save()

    return jsonify(list_item.serialize), 201


@todo_list_api.route('/todo/<id>/complete/', methods=['PATCH'])
@auth.login_required
def toggle_item_completed(id):
    item = TodoListItem.query.filter_by(user_id=g.user.id, id=id).first()
    if not item:
        return jsonify({'error': '404 not found'}), 404
    
    item.is_completed = not item.is_completed
    item.save()

    return jsonify(item.serialize), 200


@todo_list_api.route('/todo/<id>/update/', methods=['PATCH'])
@auth.login_required
def update_todo_list_item(id):
    request_json = request.get_json()
    item = TodoListItem.query.filter_by(user_id=g.user.id, id=id).first()
    if not item:
        return jsonify({'error': '404 not found'}), 404

    try:
        item.update(request_json)
    except:
        return jsonify({'error': 'cannot update values {}'.format(request_json)}), 400

    return jsonify(item.serialize), 200


@todo_list_api.route('/todo/<id>/delete/', methods=['DELETE'])
@auth.login_required
def delete_todo_list_item(id):
    TodoListItem.query.filter_by(user_id=g.user.id, id=id).delete()
    db_session.commit()

    return jsonify({}), 200