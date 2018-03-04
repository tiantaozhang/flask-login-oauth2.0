#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
from logging.handlers import TimedRotatingFileHandler
from flask import jsonify
from flask_script import Manager, Shell, Server
from apps import create_app
# from admin.exception import YMException

FLASK_CONFIG = os.getenv("FLASK_CONFIG", "default")
app = create_app(FLASK_CONFIG)

# logger config
handler = TimedRotatingFileHandler(
    app.config['APP_LOG_FILE'],
    when='D',
    backupCount=15
)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)


# @apps.errorhandler(YMException)
# def handle_http_exception(error):
#     """细化处理请求错误，返回响应
#     :param error: HTTPException instance
#     :return: response
#     """
#     if error.logging:
#         apps.logger.error(error.message, exc_info=sys.exc_info)
#     if error.sentry_alarm:
#         from admin import sentry_client
#         sentry_client.captureException()
#     return jsonify({'c': error.code, 'm': error.message})
#
# @apps.errorhandler(404)
# def handle_404_exception(error):
#     """处理逻辑错误，返回响应
#     :param error: Exception instance
#     :return: response
#     """
#     return jsonify({'c': error.code, 'm': str('你请求的页面不存在=。=')})

# @apps.errorhandler(Exception)
# def handle_all_exception(error):
#     """处理逻辑错误，返回响应
#     :param error: Exception instance
#     :return: response
#     """
#     apps.logger.error(str(error.args[0]), exc_info=sys.exc_info)
#     from admin import sentry_client
#     sentry_client.captureException()
#     return jsonify({'c': 500, 'm': str('系统内部错误，请联系管理员解决！')})


manager = Manager(app)

def make_shell_context():
    return dict(app=app)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('runserver', Server(host="0.0.0.0", port=9000))

if __name__ == "__main__":
    manager.run()
