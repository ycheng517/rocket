from __future__ import print_function
from pymongo import MongoClient
from datetime import datetime, timedelta


class PlayerAvgStats:

    def __init__(self, collection):
        # this is expecting a mongo collection
        self.collection = collection
        self.collection.remove({})

    def calc_avg_stats(self, game_logs):        
        avg_stats = game_logs.aggregate([
            {
                "$group": {
                    "_id": {
                        "PLAYER_NAME": "$PLAYER_NAME",
                        "PLAYER_ID": "$PLAYER_ID",
                        "SEASON_ID": "$SEASON_ID",
                        "TEAM_ABBREVIATION": "$TEAM_ABBREVIATION"
                    },
                    "GAMES_PLAYED": { "$sum": 1 },
                    "AVG_MIN": {"$avg": "$MIN"},
                    "AVG_PTS": {"$avg": "$PTS"},
                    "AVG_FGM": {"$avg": "$FGM"},
                    "AVG_FGA": {"$avg": "$FGA"},
                    "AVG_FG3M": {"$avg": "$FG3M"},
                    "AVG_FG3A": {"$avg": "$FG3A"},
                    "AVG_FTM": {"$avg": "$FTM"},
                    "AVG_FTA": {"$avg": "$FTA"},
                    "AVG_REB": {"$avg": "$REB"},
                    "AVG_OREB": {"$avg": "$OREB"},
                    "AVG_DREB": {"$avg": "$DREB"},
                    "AVG_AST": {"$avg": "$AST"},
                    "AVG_STL": {"$avg": "$STL"},
                    "AVG_BLK": {"$avg": "$BLK"},
                    "AVG_PLUS_MINUS": {"$avg": "$PLUS_MINUS"},
                    "AVG_TOV": {"$avg": "$TOV"},
                    "AVG_PF": {"$avg": "$PF"}
                }
            }
        ])
        count = 0
        for document in avg_stats:
            count += 1
            print(count)
            self.collection.update_one(
                {
                    "PLAYER_NAME": document["_id"]["PLAYER_NAME"],
                    "PLAYER_ID": document["_id"]["PLAYER_ID"],
                    "SEASON_ID": document["_id"]["SEASON_ID"],
                    "TEAM_ABBREVIATION": document["_id"]["TEAM_ABBREVIATION"]
                 },
                {
                    "$set": {
                         "GAMES_PLAYED": document["GAMES_PLAYED"],
                         "AVG_MIN": document["AVG_MIN"],
                         "AVG_PTS": document["AVG_PTS"],
                         "AVG_FGM": document["AVG_FGM"],
                         "AVG_FGA": document["AVG_FGA"],
                         "AVG_FG3M": document["AVG_FG3M"],
                         "AVG_FG3A": document["AVG_FG3A"],
                         "AVG_FTM": document["AVG_FTM"],
                         "AVG_FTA": document["AVG_FTA"],
                         "AVG_REB": document["AVG_REB"],
                         "AVG_OREB": document["AVG_OREB"],
                         "AVG_DREB": document["AVG_DREB"],
                         "AVG_AST": document["AVG_AST"],
                         "AVG_STL": document["AVG_STL"],
                         "AVG_BLK": document["AVG_BLK"],
                         "AVG_PLUS_MINUS": document["AVG_PLUS_MINUS"],
                         "AVG_TOV": document["AVG_TOV"],
                         "AVG_PF": document["AVG_PF"]
                     }
                 },
                upsert=True
            )
