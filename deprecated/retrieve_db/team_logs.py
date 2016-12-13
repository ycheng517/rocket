from __future__ import print_function
from nba_py import league
from pymongo import MongoClient


class TeamLogs:
    seasons = ['2014-15', '2015-16']

    def __init__(self, collection):
        # this is expecting a mongo collection
        self.collection = collection
        self.empty_collection()
        self.load_collection()
        pass

    def load_collection(self, seasons=seasons):
        for season in seasons:
            ap = league.GameLog(player_or_team='T', season=season)
            logs = ap.overall()
            self.collection.insert_many(logs.to_dict('records'))

    def empty_collection(self):
        self.collection.remove({})
