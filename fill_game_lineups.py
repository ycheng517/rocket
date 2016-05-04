from pymongo import MongoClient
from bson.code import Code
from nba_py.constants import *
import sys

assert str(sys.argv[1]) is not None
client = MongoClient(str(sys.argv[1]))
db = client.nba_py

lineups = db.game_lineups.find()
count = 0
for lineup in lineups: 
    count += 1
    print(count)
    roster = db.rosters.find_one({"SEASON_ID": lineup['SEASON_ID'], 
                                  "TEAM_ABBREVIATION": lineup['TEAM_ABBREVIATION']})
    for player_id in roster['roster']: 
        if player_id not in lineup['lineup'].keys():
            db.game_lineups.update_one(
                    {
                        "_id": lineup['_id']
                     },
                    {
                        "$set": {
                             ("lineup." + player_id): 1
                         }
                     }
                )