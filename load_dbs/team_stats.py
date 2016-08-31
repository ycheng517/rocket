from nba_py import team
from pymongo import MongoClient
from nba_py.constants import TEAMS, MeasureType

seasons = ['2013-14', '2014-15', '2015-16']

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
client = MongoClient("52.41.52.130", 27017)
db = client.nba_stats

for season in seasons:
    for t in teams:
        general_splits = team.TeamGeneralSplits(t['TEAM_ID'])
        print ("getting stats for %s" % t['TEAM_ID'])
        logs = general_splits.overall()
        for log in logs:
            log['TEAM_ID'] = t['TEAM_ID']
        db.team_stats.insert_many(logs)
        general_splits = team.TeamGeneralSplits(t['TEAM_ID'], measure_type=MeasureType.Opponent)
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

