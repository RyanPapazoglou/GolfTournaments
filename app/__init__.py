import os
import datetime
import pytz
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
m = Migrate(compare_type=True)
login = LoginManager()
bootstrap = Bootstrap()

local = pytz.timezone('US/Eastern')
TIMEOUT = os.getenv('TEAM_BUILDER_TIMEOUT') if os.getenv('TEAM_BUILDER_TIMEOUT') else '05/08/2020 23:59:59'
START_TIME = datetime.datetime.strptime(TIMEOUT, '%d/%m/%Y %H:%M:%S')
CURRENT_TIME = datetime.datetime.now()

print(START_TIME)
print(CURRENT_TIME)
print(CURRENT_TIME > START_TIME)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(os.environ["APP_SETTINGS"])
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    m.init_app(app=app, db=db)
    login.init_app(app=app)
    login.login_view = 'auth.login'
    bootstrap.init_app(app=app)

    with app.app_context():
        from app.models import Users, Golfers, UsersGolfers
        from app import index
        from app.auth import auth_routes
        from app.profile import profile_routes, profile_dao
        from app.golfers import golfers_routes, golfers_dao
        from app.errors import page_not_found, internal_error

        app.register_blueprint(index.bp)
        app.register_blueprint(auth_routes.bp)
        app.register_blueprint(profile_routes.bp)
        app.register_blueprint(golfers_routes.bp)
        app.register_error_handler(404, page_not_found)
        app.register_error_handler(500, internal_error)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()