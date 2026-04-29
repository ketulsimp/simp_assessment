from pymongo import AsyncMongoClient

client=AsyncMongoClient('mongodb://localhost:27017')
db=client['test']
users=db['users']
tasks=db['tasks']