from nba_py import team
from pymongo import MongoClient
from nba_py.constants import TEAMS, MeasureType


class TeamStats:
    seasons = ['2014-15', '2015-16']

    def __init__(self, collection):
        # this is expecting a mongo collection
        self.collection = collection
        self.empty_collection()
        self.load_collection()

    def load_collection(self, seasons=seasons):
        for season in seasons:
            for team_name in TEAMS.itervalues():
                ap = team.TeamGeneralSplits(team_id=team_name['id'], 
                                            season=season)
                results = ap.location().to_dict('records')
                records = {}
                
                for item in results:
                    self.collection.update_one({
                        "TEAM_ID": team_name['id'],
                        "TEAM_ABBREVIATION": team_name['abbr'],
                        "SEASON_ID": str(2) + season[:4]}, 
                       {"$set": {
                                 item['TEAM_GAME_LOCATION'] + '_WIN': item['W'],
                                 item['TEAM_GAME_LOCATION'] + '_LOSS': item['L'],
                                 item['TEAM_GAME_LOCATION'] + '_WIN_PCT': item['W_PCT']
                                 }},
                       upsert=True)

    def empty_collection(self):
        self.collection.remove({})
