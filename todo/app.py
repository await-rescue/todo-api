from flask import Flask, request, abort, redirect
# from flask_login import LoginManager, login_user
from db import db_session, init_db

from views import user_views, todo_list_views
from models import User

app = Flask(__name__)

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "login"

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


# @login_manager.user_loader
# def load_user(email):
#     return User.query.filter_by(email=email).first()


# @app.route('/login/', methods=['GET, POST'])
# def login():
#     # get the user to check password
#     email = request.get_json().get('email')
#     password = request.get_json().get('password')
#     user = User.query.filter_by(email=email)
#     if user.check_password(password):
#         login_user(user)
#     else:
#         return abort(401)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')