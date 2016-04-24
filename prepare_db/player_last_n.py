from __future__ import print_function
from pymongo import MongoClient
from datetime import datetime, timedelta


class PlayerLastN:

    def __init__(self, collection):
        # this is expecting a mongo collection
        self.collection = collection

    def calc_last_N(self, prior_days=14, lastN=5, batch_size=50):
        logs = self.collection.find().batch_size(batch_size)
        field_name = "AVG_PTS_LAST_" + lastN
        for log in logs:
            #===========================================================================
            # print("===========================================================")
            # print('player ID: %d, date: %s' % (log['PLAYER_ID'], log['GAME_DATE']))
            #===========================================================================
            time_prior = datetime.strptime(log['GAME_DATE'], '%Y-%m-%d') \
                - timedelta(days=prior_days)
            time_prior = time_prior.strftime("%Y-%m-%d")
            games_last_N = self.collection.aggregate([
                {"$match": {
                    "GAME_DATE": {
                        "$lt": log['GAME_DATE'],
                        "gt": time_prior
                    }, 
                    "PLAYER_ID": log['PLAYER_ID'],
                    "SEASON_ID": log['SEASON_ID']
                    }
                }, 
                {"$sort": {"GAME_DATE": -1}},
                {"$limit": lastN},
                {
                    "$group": {
                        "_id": {
                            "PLAYER_ID": "$PLAYER_ID", 
                            "SEASON_ID": "$SEASON_ID"
                        },
                        field_name: {"$avg": "$PTS"}
                    }
                }
            ])
            if games_last_N is None:
                self.collection.update_one(
                    {
                        "_id": log['_id']
                     },
                    {
                        "$set": {
                             field_name: log["AVG_PTS"]
                         }
                     },
                    upsert=True
                )
            for document in games_last_N:
                self.collection.update_one(
                    {
                        "_id": log['_id']
                     },
                    {
                        "$set": {
                             field_name: document[field_name]
                         }
                     },
                    upsert=True
                )
            #FOR VERIFICATION
            #===========================================================================
            # games_last_5 = db.model.aggregate([
            #     {"$match": {
            #         "GAME_DATE": {
            #             "$lt": log['GAME_DATE']
            #         }, 
            #         "PLAYER_ID": log['PLAYER_ID'], 
            #         "SEASON_ID": log['SEASON_ID']
            #         }
            #     }, 
            #     {"$sort": {"GAME_DATE": -1}},
            #     {"$limit": 5},
            #     {
            #         "$group": {
            #             "_id": {
            #                 "PLAYER_ID": "$PLAYER_ID",
            #                 "SEASON_ID": "$SEASON_ID",
            #                 "GAME_DATE": "$GAME_DATE", 
            #                 "PTS": "$PTS"
            #             }
            #         }
            #     }
            # ])
            # for document in games_last_5:
            #     print(document)
            #===========================================================================
