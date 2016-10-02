from nba_py import team
from pymongo import MongoClient
from nba_py.constants import MeasureType

seasons = ['2007-08', '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16']
team_list = team.TeamList()
team_list_list = team_list.info()
count = 0
teams = []
for t in team_list_list:
    if t['ABBREVIATION'] is not None:
            count +=1
            teams.append(t)
            print t
print count
client = MongoClient("52.41.48.61", 27017)
db = client.nba_stats
db.team_stats.drop()
db.team_opponent_stats.drop()

for season in seasons:
    for t in teams:
        general_splits = team.TeamGeneralSplits(t['TEAM_ID'], season=season)
        print ("getting stats for %s" % t['TEAM_ID'])
        logs = general_splits.overall()
        for log in logs:
            log['TEAM_ID'] = t['TEAM_ID']
        db.team_stats.insert_many(logs)
        general_splits = team.TeamGeneralSplits(t['TEAM_ID'], measure_type=MeasureType.Opponent, season=season)
        logs = general_splits.overall()
        for log in logs:
            log['TEAM_ID'] = t['TEAM_ID']
        db.team_opponent_stats.insert_many(logs)
        #===========================================================================
        # players_list = logs.to_dict('records')
        # for d in players_list: 
        #     
        # print (players_list)
        #===========================================================================

