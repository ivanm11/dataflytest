from datafly.users.mixins import UserMixin
from datafly.odm import Document

class User(UserMixin, Document):
    __collection__ = 'users'
    __cookie__ = 'user'
