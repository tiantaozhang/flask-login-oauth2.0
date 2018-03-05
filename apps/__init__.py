# coding=utf-8

# from raven.contrib.flask import Sentry
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from admin.utils.AlchemyEncoder import AlchemyEncoder
from flask_login import LoginManager
from config.app_setting import config

# import boto3
# import redis

login_manager = LoginManager()
# login_manager.session_protection = 'strong'
# login_manager_view = 'auth.login'

db = SQLAlchemy()

sentry_client = None

s3 = None

# 本地redis
# redis_local_db = redis.StrictRedis(host='localhost', port=6379, db=0)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # apps.json_encoder = AlchemyEncoder

    login_manager.init_app(app)
    db.init_app(app)
    # db.reflect(apps=apps)

    # init raven
    # global sentry_client
    # sentry_client = Sentry(app, dsn=config[config_name].SENTRY_DSN)

    from apps.view import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


from config.app_setting import IS_DATABASE
from apps.models.user import User
@login_manager.user_loader
def load_user(id):
    if not IS_DATABASE:
        from apps.models.user import USERS
        return USERS.get(int(id))
    else:
        return User.query.get(id)