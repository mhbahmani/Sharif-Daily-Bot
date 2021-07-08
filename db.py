from pymongo import MongoClient


class DB:

    def __init__(self) -> None:
        self.db = MongoClient().sharifdailybot