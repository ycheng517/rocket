from nba_py import league
from pymongo import MongoClient

seasons = ['2007-08', '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16']

client = MongoClient("52.41.48.61", 27017)
db = client.nba_stats
db.player_avg_stats.drop()
for season in seasons:
    ap = league.PlayerStats(season=season)
    logs = ap.overall()
    for log in logs:
        print(log)
        log["SEASON_ID"] = "2" + season[:4]
    db.player_avg_stats.insert_many(logs)
    #===========================================================================
    # players_list = logs.to_dict('records')
    # for d in players_list: 
    #     
    # print (players_list)
    #===========================================================================

