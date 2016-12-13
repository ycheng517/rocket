from __future__ import print_function
from nba_py import team
from pymongo import MongoClient
from nba_py.constants import *

class TeamOppLogs:
    seasons = ['2014-15', '2015-16']

    def __init__(self, collection):
        # this is expecting a mongo collection
        self.collection = collection
        self.empty_collection()
        self.load_collection()
        pass

    def load_collection(self, seasons=seasons):
        for season in seasons:
            for team_name in TEAMS.itervalues():
                ap = team.TeamGeneralSplits(team_id=team_name['id'], 
                                            measure_type=MeasureType.Opponent, season=season)
                logs = ap.overall()
                self.collection.insert_many(logs.to_dict('records'))

    def empty_collection(self):
        self.collection.remove({})
