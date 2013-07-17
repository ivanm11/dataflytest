from pymongo import Connection

from config import Config

# Mongo DB
connection = Connection(Config.MONGO['host'], Config.MONGO['port'])
db = connection[Config.DB]

def init_db():
    from models import User
    beginner = { 'email': 'demo@datafly.net' }
    exists = User.find_one(beginner)
    if not exists:
        u = User(beginner)
        u.encrypt_password('demo')