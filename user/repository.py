import json
from pymongo import MongoClient
from env import USE_MONGO, MONGO_URL

USERS_FILE = "{}/data/users.json"

def get_repository():
    if USE_MONGO:
        return MongoUserRepository()
    return JsonUserRepository()

class JsonUserRepository:
    def load(self):
        with open(USERS_FILE.format("."), "r") as file:
            return json.load(file)["users"]

    def save(self, users):
        with open(USERS_FILE.format("."), "w") as file:
            json.dump({"users": users}, file)

class MongoUserRepository:
    def __init__(self):
        self.client = MongoClient(MONGO_URL)
        self.db = self.client.get_database()
        self.collection = self.db["users"]

    def load(self):
        return list(self.collection.find({}))

    def save(self, users):
        self.collection.delete_many({})
        if users:
            self.collection.insert_many(users)
