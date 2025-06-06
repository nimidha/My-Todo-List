import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'your_secret_key'

    # ✅ Correct way to point to SQLite in Flask's instance folder
    db_path = os.path.join(app.instance_path, 'todo.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Make sure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    db.init_app(app)

    from app.routes import todo_routes
    app.register_blueprint(todo_routes)

    migrate = Migrate(app, db)

    return app
