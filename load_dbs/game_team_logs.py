from nba_py import game
from pymongo import MongoClient
from Queue import Queue
from threading import Thread

seasons = ['2013-14', '2014-15', '2015-16']



client = MongoClient("52.41.48.61", 27017)
db = client.nba_stats
db.game_team_logs.drop()

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
        db.game_team_logs.insert_many(team_logs) # to_dict because of Pandas
        q.task_done()
        
for i in range(num_worker_threads):
    t = Thread(target=worker)
    t.daemon = True
    t.start()

q.join()

