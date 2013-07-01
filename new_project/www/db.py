from pymongo import Connection

from config import Config

# Mongo DB
connection = Connection(Config.MONGO['host'], Config.MONGO['port'])
db = connection[Config.DB]

def init_db():
    pass