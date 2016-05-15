from __future__ import print_function
from threading import Thread
from nba_py import league
from nba_py import game
from pymongo import MongoClient
import Queue

class GameLogs:
    seasons = ['2014-15', '2015-16']

    def __init__(self, collection):
        # this is expecting a mongo collection
        self.collection = collection
        self.q = Queue.Queue()
        #self.empty_collection()
        #self.load_collection()
        pass

    def load_collection(self, seasons=seasons):
        for season in seasons:
            ap = league.GameLog(season=season)
            logs = ap.overall()
            self.collection.insert_many(logs.to_dict('records'))

    def empty_collection(self):
        self.collection.remove({})
        
    def add_team_ids(self, team_logs):
        count = 0
        logs = team_logs.find()
        all_game_logs = []
        for log in logs:
            count += 1
            print(count)
            all_game_logs.append(log)
            
        num_worker_threads = 10
        for i in range(num_worker_threads):
            t = Thread(target=self.process_boxscore_summary)
            t.daemon = True
            t.start()
        
        for item in all_game_logs:
            self.q.put(item)
        
        self.q.join()       # block until all tasks are done
    
    def process_boxscore_summary(self):
        while True:
            log = self.q.get()
            ap = game.Boxscore(game_id=log['GAME_ID'])
            summary = ap.game_summary().to_dict('records')
            self.collection.update_many({"GAME_ID": log['GAME_ID'],
                            "TEAM_ABBREVIATION": log['TEAM_ABBREVIATION']},
                           {"$set": {"TEAM_ID": log['TEAM_ID'],
                            "HOME_TEAM_ID": summary[0]['HOME_TEAM_ID'],
                            "VISITOR_TEAM_ID": summary[0]['VISITOR_TEAM_ID']}})
            self.q.task_done()
