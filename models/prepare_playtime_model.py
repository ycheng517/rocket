from __future__ import print_function
from pymongo import MongoClient
from datetime import datetime, timedelta
from pip._vendor.progress import counter


class PlaytimeModel:

    def __init__(self, collection):
        # this is expecting a mongo collection
        self.collection = collection
        self.collection.remove({})

    def load_minutes(self, game_logs):
        count = 0
        logs = game_logs.find()
        for log in logs:
            count += 1
            print(count)
            self.collection.insert_one({
                                        "GAME_ID": log['GAME_ID'],
                                        "SEASON_ID": log['SEASON_ID'],
                                        "GAME_DATE": log['GAME_DATE'],
                                        "TEAM_ABBREVIATION": log['TEAM_ABBREVIATION'],
                                        "PLAYER_ID": log['PLAYER_ID'],
                                        "MIN": log['MIN']
                                        })

    def load_lineups(self, game_lineups):
        count = 0
        minute_logs = self.collection.find()
        for log in minute_logs:
            count += 1
            print(count)
            lineup = game_lineups.find_one({
                                  "GAME_ID": log['GAME_ID'], 
                                  "TEAM_ABBREVIATION": log['TEAM_ABBREVIATION']})
            self.collection.update_one({
                                        "_id": log['_id']
                                        },
                                       {"$set": {
                                                "lineup": lineup['lineup']}
                                        })
        
    def load_avg_min(self):
        count = 0
        logs = self.collection.find()
        for log in logs:
            count += 1
            print(count)
            avg_mins = self.collection.aggregate([
                {"$match": {
                    "PLAYER_ID": log['PLAYER_ID'],
                    "SEASON_ID": log['SEASON_ID']
                    }
                 },
                {
                    "$group": {
                        "_id": {
                            "PLAYER_ID": "$PLAYER_ID",
                            "SEASON_ID": "$SEASON_ID"
                        },
                        "AVG_MIN": {"$avg": "$MIN"}
                    }
                }
            ])
            for document in avg_mins:
                self.collection.update_one(
                    {
                        "_id": log['_id']
                     },
                    {
                        "$set": {
                             "AVG_MIN": document["AVG_MIN"]
                         }
                     }
                )

