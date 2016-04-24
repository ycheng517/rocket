from __future__ import print_function
from nba_py import league
from pymongo import MongoClient


class TeamLogs:
    seasons = ['2011-12', '2012-13', '2013-14', '2014-15', '2015-16']

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.nba_py
        self.empty_collection()
        self.load_collection()
        pass

    def load_collection(self, seasons=seasons):
        for season in seasons:
            ap = league.GameLog(season=season)
            logs = ap.overall()
            self.db.game_logs.insert_many(logs.to_dict('records'))

    def empty_collection(self):
        self.db.game_logs.remove({})
