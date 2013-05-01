from pymongo import Connection

# Mongo DB
connection = Connection('localhost', 27017)
db = connection.new_project