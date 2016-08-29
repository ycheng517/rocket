from nba_py import league
from nba_py.constants import TEAMS
from pymongo import MongoClient

seasons = ['2013-14', '2014-15', '2015-16']

client = MongoClient()
db = client.nba_stats

#===============================================================================
# for season in seasons:
#     ap = league.GameLog(season=season)
#     logs = ap.overall()
#     print(len(logs))
#     db.game_stats.insert_many(logs)
#===============================================================================

game_logs = db.game_stats.find()
for log in game_logs:
    team_id = TEAMS[log['TEAM_ABBREVIATION']]['id']
    db.game_stats.update_one({"_id": log['_id']},
                             {'$set':
                                {"TEAM_ID": team_id}})
    #===========================================================================
    # players_list = logs.to_dict('records')
    # for d in players_list: 
    #     
    # print (players_list)
    #===========================================================================

