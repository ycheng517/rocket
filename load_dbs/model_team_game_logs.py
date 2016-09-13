import pymongo
import numpy
from Queue import Queue
from threading import Thread

client = pymongo.MongoClient("52.41.48.61", 27017)
db = client.nba_stats

q = Queue()
results = db.team_game_logs.find({})
for result in results:
    q.put(result)
    
num_worker_threads = 8
global count
count = 0

def worker():
    global count
    while True:
        item = q.get()
        count += 1
        print count
        results = db.basic_model.update_many({'GAME_ID': item['GAME_ID'],
                                    'TEAM_ID': str(item['TEAM_ID'])},
                                   {'$set': {'TEAM_GAME_PTS': item['PTS'],
                                            'TEAM_GAME_FGM': item['FGM'],
                                            'TEAM_GAME_FGA': item['FGA'],
                                            'TEAM_GAME_FG3M': item['FG3M'],
                                            'TEAM_GAME_FG3A': item['FG3A'],
                                            'TEAM_GAME_FTM': item['FTM'],
                                            'TEAM_GAME_FTA': item['FTA'],
                                            'TEAM_GAME_REB': item['REB'],
                                            'TEAM_GAME_DREB': item['DREB'],
                                            'TEAM_GAME_AST': item['AST'],
                                            'TEAM_GAME_STL': item['STL'],
                                            'TEAM_GAME_BLK': item['BLK'],
                                            'TEAM_GAME_PF': item['PF'],
                                            'TEAM_GAME_TOV': item['TO']}},
                                   upsert=False)
        print results
        q.task_done()
        
for i in range(num_worker_threads):
    t = Thread(target=worker)
    t.daemon = True
    t.start()

q.join()       # block until all tasks are done