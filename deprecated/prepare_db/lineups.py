from __future__ import print_function
from pymongo import MongoClient
from datetime import datetime, timedelta

class GameLineups:

    def __init__(self, collection):
        # this is expecting a mongo collection
        self.collection = collection
        self.collection.remove({})

    def calc_game_lineups(self, game_logs, team_logs, batch_size=10):
        count = 0
        games = team_logs.find()
        for game in games:
            count += 1
            print(count)
            players = game_logs.find({
                          "GAME_ID": game['GAME_ID'],
                          "TEAM_ABBREVIATION": game['TEAM_ABBREVIATION'], 
                          #to filter out players playing because of garbage time
                          #maybe a good thing to filter out players leaving game
                          #early due to injury as well
                          "MIN": {"$gt": 10}})
            for player in players:
                self.collection.update_one(
                    {
                        "GAME_ID": game['GAME_ID'], 
                        "TEAM_ABBREVIATION": game['TEAM_ABBREVIATION'],
                        "SEASON_ID": game['SEASON_ID']
                     },
                    {
                        "$push": { "lineup": player['PLAYER_ID'] }
                     },
                    upsert=True
                )
