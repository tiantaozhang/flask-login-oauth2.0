from flask import Blueprint, request
# from cerberus import Validator
# from admin.exception import BadRequest, YMException

main = Blueprint("main", __name__)
main.config = {}


# @main.record
# def record_params(setup_state):
#     apps = setup_state.apps
#     main.config = dict([(key, value) for (key, value) in apps.config.items()])


from . import login