from __future__ import print_function
from nba_py import league
from nba_py import game
from pymongo import MongoClient


class GameLogs:
    seasons = ['2014-15', '2015-16']

    def __init__(self, collection):
        # this is expecting a mongo collection
        self.collection = collection
        #self.empty_collection()
        #self.load_collection()
        pass

    def load_collection(self, seasons=seasons):
        for season in seasons:
            ap = league.GameLog(season=season)
            logs = ap.overall()
            self.collection.insert_many(logs.to_dict('records'))

    def empty_collection(self):
        self.collection.remove({})
        
    def add_team_ids(self, team_logs):
        count = 0
        logs = team_logs.find()
        for log in logs:
            count += 1
            print(count)
            ap = game.Boxscore(game_id=log['GAME_ID'])
            summary = ap.game_summary().to_dict('records')
            self.collection.update_many({"GAME_ID": log['GAME_ID'],
                                    "TEAM_ABBREVIATION": log['TEAM_ABBREVIATION']},
                                   {"TEAM_ID": log['TEAM_ID'],
                                    "HOME_TEAM_ID": summary[0]['HOME_TEAM_ID'],
                                    "AWAY_TEAM_ID": summary[0]['AWAY_TEAM_ID']})
            
