from nba_py import league, team
from pymongo import MongoClient
from Queue import Queue
from threading import Thread

seasons = ['2007-08', '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16']

team_list = team.TeamList().info()
team_dict = {}
for team in team_list:
    team_dict[team['ABBREVIATION']] = team

client = MongoClient("52.41.48.61", 27017)
db = client.nba_stats
db.game_logs.drop()

for season in seasons:
    ap = league.GameLog(season=season)
    logs = ap.overall()
    print(len(logs))
    print season
    db.game_logs.insert_many(logs)

q = Queue()
game_logs = db.game_logs.find()
for log in game_logs:
    q.put(log)


global count
count = 0

def worker():
    while True:
        log = q.get()
        global count
        count += 1
        if count % 100 == 0:
            print count
        if log['TEAM_ABBREVIATION'] == 'NOK' or log['TEAM_ABBREVIATION'] == 'NOH':
            team_id = team_dict['NOP']['TEAM_ID']
        elif log['TEAM_ABBREVIATION'] == 'SEA':
            team_id = team_dict['OKC']['TEAM_ID']
        elif log['TEAM_ABBREVIATION'] == 'NJN':
            team_id = team_dict['BKN']['TEAM_ID'] 
        else:
            team_id = team_dict[log['TEAM_ABBREVIATION']]['TEAM_ID']
        db.game_logs.update_one({"_id": log['_id']},
                                 {'$set':
                                    {"TEAM_ID": int(team_id)}})
        q.task_done()

for t in range(8):
    t = Thread(target=worker)
    t.daemon = True
    t.start()

q.join()