# coding=utf-8

# from raven.contrib.flask import Sentry
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from admin.utils.AlchemyEncoder import AlchemyEncoder
from flask_login import LoginManager
from config.app_setting import config
from flask import session, request
# import boto3
import redis

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager_view = 'auth.login'
login_manager._login_disabled = False
# login_manager.session_protection = None


db = SQLAlchemy()

sentry_client = None

s3 = None

# 本地redis
# redis_local_db = redis.StrictRedis(host='localhost', port=6379, db=0)

# 本地redis
redis_local_db = redis.StrictRedis(host='localhost', port=6379, db=0)

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
# @login_manager.user_loader
# def load_user(id):
#     if not IS_DATABASE:
#         from apps.models.user import USERS
#         return USERS.get(int(id))
#     else:
#         print 'user_loader'
#         return User.query.get(id)
#
# @login_manager.header_loader
# def load_header(header_val):
#     print header_val


@login_manager.request_loader
def load_request(request):
    token = request.headers.get('Authorization')
    if token is None:   #
        token = session.get('token')
    if token is None:
        return None

    redis_token_key = '%s' % token
    token_uid = redis_local_db.get(redis_token_key)
    print token_uid
    if token_uid:   # 延长过期时间
        redis_local_db.expire(redis_token_key, 600)
        user = User.query.get(token_uid)
        if user:
            user.is_authenticated = True
            return user
        else:
            return None
    # 过期，需重新登录
    return None


@login_manager.unauthorized_handler
def unauthrized():
    print request.view_args
    return 'Unauthorized'

