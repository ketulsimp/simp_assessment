from pymongo import MongoClient

connection = MongoClient("mongodb://localhost:27017/")
db = connection['flask_test']
users = db['users']