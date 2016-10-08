from nba_py.constants import TEAMS
import pymongo
import pprint

seasons = ['2007-08', '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16']

client = pymongo.MongoClient("52.41.48.61", 27017)
db = client.nba_stats

teams = []
for key, vals in TEAMS.iteritems():
    teams.append(TEAMS[key]['id'])
    
print teams
            
# calculate game number (out of 82)
count = 0
for season in seasons:
    for team in teams:
        all_games = db.game_summary.find({"SEASON": season[0:4], 
                                          "$or": [ { "HOME_TEAM_ID": int(team) },
                                                  { "VISITOR_TEAM_ID": int(team) } ]}).sort("GAME_DATE_EST", pymongo.ASCENDING)
        game_count = 1
        for g in all_games:
            count += 1
            print count
            db.basic_model.update_many({"GAME_ID": g["GAME_ID"], 
                                        "TEAM_ID": str(team)}, 
                                   {"$set":
                                        {"GAME_NUMBER": game_count}},
                                   upsert=False)
            game_count += 1
