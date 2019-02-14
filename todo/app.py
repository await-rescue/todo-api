from flask import Flask
from db import db_session, init_db

from views import user_view, todo_list_view

app = Flask(__name__)
app.register_blueprint(todo_list_view.todo_list_api)
app.register_blueprint(user_view.user_api)

# For this purpose, refresh the db each time
init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')