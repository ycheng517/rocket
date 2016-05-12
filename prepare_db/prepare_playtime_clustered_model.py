from __future__ import print_function
from pymongo import MongoClient


class PlaytimeModel:

    def __init__(self, collection):
        # this is expecting a mongo collection
        self.collection = collection
        self.collection.remove({})

    def load_minutes(self, game_logs, player_averages):
        count = 0
        groups = player_averages.distinct( "PLAYER_GROUP" )
        empty_groups = {}
        for group in groups: 
            empty_groups.update({str(group): 0})

        logs = game_logs.find()
        for log in logs:
            count += 1
            print(count)
            
            dataRow = {
                "GAME_ID": log['GAME_ID'],
                "SEASON_ID": log['SEASON_ID'],
                "GAME_DATE": log['GAME_DATE'],
                "TEAM_ABBREVIATION": log['TEAM_ABBREVIATION'],
                "PLAYER_ID": log['PLAYER_ID'],
                "MIN": log['MIN']}
            dataRow.update(empty_groups)
            self.collection.insert_one(dataRow)
            
    def load_lineups(self, game_lineups, player_averages):
        count = 0
        minute_logs = self.collection.find()
        for log in minute_logs:
            count += 1
            print(count)
            lineup = game_lineups.find_one({
                                  "GAME_ID": log['GAME_ID'], 
                                  "TEAM_ABBREVIATION": log['TEAM_ABBREVIATION']})
            for player in lineup['lineup']:
                teammate = player_averages.find_one({"SEASON_ID": log['SEASON_ID'],
                                          "PLAYER_ID": player, 
                                          "TEAM_ABBREVIATION": log['TEAM_ABBREVIATION']
                                          })
                self.collection.update_one({"_id": log['_id']},
                                           {"$inc": {str(teammate['PLAYER_GROUP']): 1}})
        
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