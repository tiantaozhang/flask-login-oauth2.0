# -*- coding: utf8 -*-

from apps import db
from sqlalchemy import Integer, String
from flask.ext.login import UserMixin
from config.app_setting import IS_DATABASE
import hmac, hashlib


if not IS_DATABASE:
    class User(UserMixin):
        """User Session management Class
        """
        def __init__(self, email, id, fname="", lname="", accesstoken="", active=True):
            self.email = email
            self.id = id
            self.active = active
            self.fname = fname
            self.lname = lname
            self.accesstoken = accesstoken

        def is_active(self):
            return self.active

        def myemail(self):
            return self.email

        def get_userid(self):
            return self.id

        def get_fname(self):
            return self.fname

        def get_lname(self):
            return self.lname


    """
    如果没有数据库，用USERS代替
    """

    USERS = {
        "1": User("admin@gmail.com", 1, "admin", "zhang", "", True)
    }

    USER_NAMES = dict((u.email, u) for u in USERS.itervalues())
else:
    class User(db.Model, UserMixin):
        """
        User Session management Class
        """

        __tablename__ = "user"
        __table_args__ = {"schema": "ep_data"}

        id = db.Column('id', Integer, primary_key=True)
        email = db.Column(String)

        def __init__(self, email, accesstoken=""):
            self.email = email
            self.accesstoken = accesstoken

        def is_active(self):
            u = User.query.get(self.id)
            if u:
                return True
            else:
                return False

        def is_authenticated(self):
            return True

        def myemail(self):
            return self.email

        def hmac_md5(self, s):
            return hmac.new(('%s' % self.id).encode('utf-8'), ('%s' % s).encode('utf-8'), hashlib.md5).hexdigest()