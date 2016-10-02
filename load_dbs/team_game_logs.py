from nba_py import game
from pymongo import MongoClient
from Queue import Queue
from threading import Thread

client = MongoClient("52.41.48.61", 27017)
db = client.nba_stats
db.team_game_logs.drop()

game_ids = db.game_logs.distinct("GAME_ID")
print(len(game_ids))

q = Queue()
num_worker_threads = 6

for game_id in game_ids:
    q.put(game_id)

print q.qsize()

global count
count = 0

def worker():
    global count
    while True:
        count += 1
        print count
        game_id = q.get()
        team_logs = game.Boxscore(str(game_id)).line_score()
        def add_opp_stats(dct, a, b):
            dct[a]['OPP_TEAM_ID'] = dct[b]['TEAM_ID']
            dct[a]['OPP_TEAM_NAME'] = dct[b]['TEAM_NAME']
            dct[a]['OPP_PTS'] = dct[b]['PTS']
            dct[a]['OPP_FGM'] = dct[b]['FGM']
            dct[a]['OPP_FGA'] = dct[b]['FGA']
            dct[a]['OPP_FG3M'] = dct[b]['FG3M']
            dct[a]['OPP_FG3A'] = dct[b]['FG3A']
            dct[a]['OPP_FTM'] = dct[b]['FTM']
            dct[a]['OPP_FTA'] = dct[b]['FTA']
            dct[a]['OPP_REB'] = dct[b]['REB']
            dct[a]['OPP_OREB'] = dct[b]['OREB']
            dct[a]['OPP_DREB'] = dct[b]['DREB']
            dct[a]['OPP_AST'] = dct[b]['AST']
            dct[a]['OPP_STL'] = dct[b]['STL']
            dct[a]['OPP_BLK'] = dct[b]['BLK']
            dct[a]['OPP_TO'] = dct[b]['TO']
            dct[a]['OPP_PF'] = dct[b]['PF']
            dct[a]['OPP_PLUS_MINUS'] = dct[b]['PLUS_MINUS']
        add_opp_stats(team_logs, 0, 1)
        add_opp_stats(team_logs, 1, 0)
        db.team_game_logs.insert_many(team_logs)
        q.task_done()

for i in range(num_worker_threads):
    t = Thread(target=worker)
    t.daemon = True
    t.start()

q.join()

game_ids = db.team_game_logs.distinct("GAME_ID")
count = 0
for game_id in game_ids:
    count += 1
    print count
    ap = game.BoxscoreSummary(game_id=game_id)
    game_date = ap.game_info()[0]['GAME_DATE']
    db.team_game_logs.update_many({"GAME_ID": game_id},
                                  {"$set":
                                   {"GAME_DATE": game_date}}, upsert=False)

