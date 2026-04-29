from pymongo import MongoClient
import os 

client= MongoClient("mongodb://localhost:27017")
database= client["final_asssessment_5"]

user_collection = database["users"]
task_collection = database["task"]
