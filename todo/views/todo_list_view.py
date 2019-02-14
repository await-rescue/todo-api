from flask import jsonify, request, Blueprint
from models import TodoListItem

todo_list_api = Blueprint('todo_api', __name__)

# TODO: auth and filter by user_id
@todo_list_api.route('/todo/', methods=['GET'])
def get_todo_list():
    # items = TodoListItem.query.filter(TodoListItem.user_id = 1)
    items = TodoListItem.query.all()
    return jsonify(results=[i.serialize for i in items]), 200


@todo_list_api.route('/todo/create/', methods=['POST'])
def create_todo_list_item():
    request_json = request.get_json()
    list_item = TodoListItem(
        text=request_json.get('text'),
        user_id=1
    )
    list_item.save()

    return jsonify(list_item.serialize), 200