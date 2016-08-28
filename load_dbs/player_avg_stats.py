from nba_py import league
from pymongo import MongoClient

seasons = ['2013-14', '2014-15', '2015-16']

client = MongoClient()
db = client.nba_stats

for season in seasons:
    ap = league.PlayerStats(season=season)
    logs = ap.overall()
    print(len(logs))
    for log in logs:
        log["SEASON_ID"] = "2" + season[:4]
    db.nba_stats.insert_many(logs)
    #===========================================================================
    # players_list = logs.to_dict('records')
    # for d in players_list: 
    #     
    # print (players_list)
    #===========================================================================

