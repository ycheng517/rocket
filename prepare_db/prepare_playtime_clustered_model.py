from __future__ import print_function
from pymongo import MongoClient


class PlaytimeModel:

    def __init__(self, collection):
        # this is expecting a mongo collection
        self.collection = collection
        
    def empty_collection(self):
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
                "PLAYER_NAME": log['PLAYER_NAME'],
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
        
    def load_avg_stats(self, player_averages):
        count = 0
        logs = self.collection.find()
        for log in logs:
            count += 1
            print(count)
            player_avg = player_averages.find_one({"PLAYER_ID": log['PLAYER_ID'],
                                             "SEASON_ID": log['SEASON_ID'],
                                             "TEAM_ABBREVIATION": log['TEAM_ABBREVIATION']
                                             })
            self.collection.update_one(
                {
                    "_id": log['_id']
                 },
                {
                    "$set": {
                         "AVG_MIN": player_avg["AVG_MIN"],
                         "PLAYER_GROUP": player_avg['PLAYER_GROUP']
                     }
                 }
            )
            
    def load_team_records(self, game_logs, team_stats):
        logs = self.collection.find()
        count = 0
        for log in logs: 
            count += 1
            print(count)
            game_log = game_logs.find_one({"GAME_ID": log['GAME_ID'], 
                                       "TEAM_ABBREVIATION": log['TEAM_ABBREVIATION']})
            print(game_log)
            home_team_pct = team_stats.find_one({"TEAM_ID": game_log['HOME_TEAM_ID'],
                                                   "SEASON_ID": game_log['SEASON_ID']})['Home_WIN_PCT']
            visitor_team_pct = team_stats.find_one({"TEAM_ID": game_log['VISITOR_TEAM_ID'],
                                                   "SEASON_ID": game_log['SEASON_ID']})['Road_WIN_PCT']
            if game_log['TEAM_ID'] == game_log['HOME_TEAM_ID']:
                win_chance = home_team_pct / visitor_team_pct
            else:
                win_chance = visitor_team_pct / home_team_pct
            self.collection.update_one({"_id": log['_id']}, 
                                   {"$set": {"WIN_CHANCE": win_chance, 
                                             "MATCHUP": log['MATCHUP']}})
        