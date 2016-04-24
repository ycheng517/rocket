from __future__ import print_function
from nba_py import league
from pymongo import MongoClient

client = MongoClient()
db = client.nba_py

seasons = ['2011-12', '2012-13', '2013-14', '2014-15', '2015-16']
for season in seasons:
    ap = league.GameLog(season=season)
    logs = ap.overall()    
    db.game_logs.insert_many(logs.to_dict('records'))
    