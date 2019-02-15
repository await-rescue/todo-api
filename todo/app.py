from flask import Flask, request, abort, redirect
from db import db_session, init_db

from views import user_views, todo_list_views
from models import User

app = Flask(__name__)
app.register_blueprint(todo_list_views.todo_list_api)
app.register_blueprint(user_views.user_api)

app.config.update(
    SECRET_KEY = 'secret_dshjhdj2jhgg87'
)

# For this purpose, refresh the db each time
init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')