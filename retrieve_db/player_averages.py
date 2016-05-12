from __future__ import print_function
from nba_py import league
from pymongo import MongoClient


class PlayerAverages:
    seasons = ['2014-15', '2015-16']

    def __init__(self, collection):
        # this is expecting a mongo collection
        self.collection = collection
        self.collection.remove({})
        self.load_collection()
        pass

    def load_collection(self, seasons=seasons):
        for season in seasons:
            ap = league.PlayerStats(season=season)
            logs = ap.overall()
            players_list = logs.to_dict('records')
            for d in players_list: 
                d["SEASON_ID"] = season
            self.collection.insert_many(players_list)

