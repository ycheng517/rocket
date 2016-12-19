from __future__ import print_function
from pymongo import MongoClient
from datetime import datetime, timedelta


class PlayerAvgPts:

    def __init__(self, collection):
        # this is expecting a mongo collection
        self.collection = collection

    def calc_avg_pts(self, batch_size=5):
        count = 0
        logs = self.collection.find()
        for log in logs:
            count += 1
            print(count)
            avg_pts = self.collection.aggregate([
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
                        "AVG_PTS": {"$avg": "$PTS"}
                    }
                }
            ])
            for document in avg_pts:
                self.collection.update_one(
                    {
                        "_id": log['_id']
                     },
                    {
                        "$set": {
                             "AVG_PTS": document["AVG_PTS"]
                         }
                     },
                    upsert=True
                )
