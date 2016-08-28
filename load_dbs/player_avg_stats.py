from nba_py import league
from pymongo import MongoClient

seasons = ['2013-14', '2014-15', '2015-16']
seasons = ['2015-16']

client = MongoClient()
db = client.nba_stats.player_avg_stats

for season in seasons:
    ap = league.PlayerStats(season=season)
    logs = ap.overall()
    print(len(logs))
    for log in logs:
        log["SEASON_ID"] = str(2)+season[:4]
    db.insert_many(logs)
    #===========================================================================
    # players_list = logs.to_dict('records')
    # for d in players_list: 
    #     
    # print (players_list)
    #===========================================================================

