from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
import pymongo

jwt=JWTManager()
mongo=PyMongo("mongodb://localhost:27017/assessment")

mongo=mongo.db.create_collection('users')