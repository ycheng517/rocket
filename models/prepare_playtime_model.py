from __future__ import print_function
from pymongo import MongoClient
from datetime import datetime, timedelta


class PlaytimeModel:

    def __init__(self, collection):
        # this is expecting a mongo collection
        self.collection = collection
        self.collection.remove({})

    def load_minutes(self, game_logs, batch_size=5):
        count = 0
        logs = self.game_logs.find()
        for log in logs:
            count += 1
            print(count)
            self.collection.insert_one({
                                        "GAME_ID": log['GAME_ID'],
                                        "GAME_DATE": log['GAME_DATE'],
                                        "TEAM_ABBREVIATION": log['TEAM_ABBREVIATION'],
                                        "PLAYER_ID": log['PLAYER_ID'],
                                        "MIN": log['MIN']
                                        })
