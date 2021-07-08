from typing import Dict
from pymongo import MongoClient


class DB:

    def __init__(self) -> None:
        self.db = MongoClient().sharifdailybot

    def add_event(self, event_data):
        self.db.events.insert_one(event_data)