import os
import json
from pymongo import MongoClient
from env import USE_MONGO, MONGO_URL

BOOKING_FILE = "{}/data/bookings.json"

def get_repository():
    if USE_MONGO:
        return MongoBookingRepository()
    return JsonBookingRepository()

class JsonBookingRepository:
    def load(self):
        with open(BOOKING_FILE.format("."), "r") as file:
            return json.load(file)["bookings"]

    def save(self, bookings):
        with open(BOOKING_FILE.format("."), "w") as file:
            json.dump({"bookings": bookings}, file)

class MongoBookingRepository:
    def __init__(self):
        self.client = MongoClient(MONGO_URL)
        self.db = self.client.get_database()
        self.collection = self.db["bookings"]

    def load(self):
        return list(self.collection.find({}))

    def save(self, bookings):
        self.collection.delete_many({})
        if bookings:
            self.collection.insert_many(bookings)
