'''
creates a document showing opponent stats for given a team ID and and game ID.
'''
import time
from Queue import Queue
import threading
from utilities import season_id_to_season


class TeamOpponentStats(object):
    def __init__(self, db):
        self.db = db
        self.q = Queue()
        self.num_games_to_process = 0
        self.num_games_processed = 0
        self.calculate_team_opponent_stats()

    def worker(self, q, num_games_to_process, num_games_processed):
        while True:
            item = q.get()
            print "processing opponent stats for the {} {} game ({}/{})".format(
                season_id_to_season(item['SEASON_ID']),
                item['MATCHUP'],
                num_games_to_process,
                num_games_processed)
            opponent_stats = self.db.team_game_logs.find({"Game_ID": item['Game_ID'],
                                                          "TEAM_ID": {"$ne": item['TEAM_ID']}
                                                          })
            assert opponent_stats.count() == 1
            for entry in opponent_stats:
                entry['OPPONENT_TEAM_ID'] = entry['TEAM_ID']
                entry['TEAM_ID'] = item['TEAM_ID']
                self.db.team_opponent_stats_logs.insert_one(entry)
                num_games_processed += 1
            q.task_done()

    def calculate_team_opponent_stats(self):
        if self.db.team_game_logs.count() == self.db.team_opponent_stats_logs.count():
            print("opponent game logs same size as team game logs, skipping")
            return
        self.db.team_opponent_stats_logs.drop()
        self.num_games_to_process = self.db.team_game_logs.count()
        results = self.db.team_game_logs.find()
        for result in results:
            self.q.put(result)

        for i in range(8):
            t = threading.Thread(target=self.worker,
                                 args=(self.q,
                                       self.num_games_to_process,
                                       self.num_games_processed))
            t.daemon = True
            t.start()

        while threading.active_count() > 0:
            time.sleep(0.1)
        self.q.join()


