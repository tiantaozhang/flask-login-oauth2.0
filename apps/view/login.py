# -*- coding: utf8 -*-

from apps.view import main
from apps.models.user import User, USERS, USER_NAMES
import requests
from flask import request, redirect
from flask.ext.login import \
    (current_user, login_required, login_user,
     logout_user, UserMixin, AnonymousUserMixin)
from config.setting import (GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET,
                            REDIRECT_URI, GOOGLE_ACCOUNTS_BASE_URL)
import json



@main.route("/")
def hello():
    if current_user.is_authenticated:
        return "User " + str(current_user.myemail()) + "is logged in"

    return "Hello World!"


@main.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect("/")


@main.route("/login")
def login():
    from apps.utils.oauth2 import GeneratePermissionUrl
    if current_user.is_authenticated:
        return current_user.get_id()

    if request.method == "GET":
        useremail = request.args.get('email', '')
        if useremail:
            if useremail in USER_NAMES:
                loginit = login_user(USER_NAMES[useremail], remember="yes")
                return "user already exists and logged in"

    if request.method == "GET" and request.args.get('email', ''):
        url = GeneratePermissionUrl(GOOGLE_CLIENT_ID, request.args.get('email', ''),
                                    redirect_uri=REDIRECT_URI, google_account_base_url=GOOGLE_ACCOUNTS_BASE_URL)
        return redirect(url)
    return "No Email Provided"


@main.route("/oauth2callback", methods=["GET"])
def oauth2callback():
    from apps.utils.oauth2 import AuthorizeTokens
    authorizationcode = request.args.get('code', '')
    useremail = request.args.get('state', '')

    response = AuthorizeTokens(GOOGLE_CLIENT_ID,
                               GOOGLE_CLIENT_SECRET,
                               authorizationcode,
                               redirect_uri=REDIRECT_URI,
                               google_account_base_url=GOOGLE_ACCOUNTS_BASE_URL)
    accesstoken = response["access_token"]

    proxies = dict(http='socks5://127.0.0.1:1080',
                   https='socks5://127.0.0.1:1080')
    r = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?access_token=' + accesstoken,
                 proxies=proxies)

    j = json.loads(r.text)

    if useremail != j['email']:
        return "e-mail和授权email不匹配"

    options = {}
    options["email"] = j.get("email")
    options["firstname"] = j.get("given_name")
    options["lastname"] = j.get("family_name")
    options["accesstoken"] = accesstoken

    if options["email"] in USER_NAMES:
        userid = USER_NAMES.get(options['email']).id
    else:
        userid = len(USERS) + 1

    u = User(options.get("email"), userid, options.get("firstname"), options.get("lastname"), accesstoken)
    USERS[userid] = u
    loginit = login_user(u, remember="yes")
    if loginit == True:
        return "Everything happened Successfullly"
    return "Some Problem happened"


