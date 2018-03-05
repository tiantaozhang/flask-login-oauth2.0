# -*- coding: utf8 -*-

from apps import db
from sqlalchemy import Integer, String
from flask.ext.login import UserMixin



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

#
# class User(db.Model, UserMixin):
#     """
#     User Session management Class
#     """
#
#     __tablename__ = "user"
#     __table_args__ = {"schema": "youmi"}
#
#     id = db.Column('uid', Integer, primary_key=True)
#     email = db.Column(String)
#
#     def __init__(self, email, id, accesstoken="", active=True):
#         self.email = email
#         self.id = id
#         self.active = active
#         self.accesstoken = accesstoken
#
#     def is_active(self):
#         return self.active



"""
如果没有数据库，用USERS代替
"""

USERS = {
    "1": User("admin@gmail.com", 1, "admin", "zhang", "", True)
}

USER_NAMES = dict((u.email, u) for u in USERS.itervalues())