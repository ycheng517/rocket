from nba_py import game
import pandas
import threading
import time
from Queue import Queue
from nba_py.constants import TEAMS

seasons = ['2007-08', '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16']


class AllGamesSummaries(object):
    def __init__(self, db):
        self.db = db
        self.q = Queue()
        # self.get_all_games_summaries()
        self.update_team_id_to_str()

    def worker(self, q):
        while True:
            game_id = q.get()
            game_summary = game.BoxscoreSummary(str(game_id)).game_summary()
            # for some reason there's duplicate records of some games,
            # so we just store the first result
            if isinstance(game_summary, pandas.DataFrame):
                game_summary = game_summary.to_dict("records")
            self.db.all_games_summaries.insert_one(game_summary[0])
            print ("%d game summaries processed" % self.db.all_games_summaries.count())
            q.task_done()

    def get_all_games_summaries(self):
        # this is a hidden dependency
        #TODO: make team_id a string
        game_ids = self.db.team_game_logs.distinct("Game_ID")
        if self.db.all_games_summaries.count() == len(game_ids):
            print ("all games summaries already exist, skip processing")
            return

        self.db.all_games_summaries.drop()
        print("gathering game summaries for %d games" % len(game_ids))
        for game_id in game_ids:
            self.q.put(game_id)

        for i in range(4):
            t = threading.Thread(target=self.worker, args=(self.q,))
            t.start()

        while threading.active_count() > 0:
            time.sleep(0.5)
        self.q.join()

    def update_team_id_to_str(self):
        print("updating team ids to string format for game summaries")
        print("*" * 30)
        sample_game = self.db.all_games_summaries.find_one()
        if isinstance(sample_game['HOME_TEAM_ID'], str) and \
            isinstance(sample_game['VISITOR_TEAM_ID'], str):
            print "team ids already in str format, skipping"
        for team in TEAMS.itervalues():
            print team['id']
            self.db.all_games_summaries.update_many({"HOME_TEAM_ID": int(team['id'])},
                                                    {"$set": {
                                                        "HOME_TEAM_ID": team['id']
                                                    }})
            self.db.all_games_summaries.update_many({"VISITOR_TEAM_ID": int(team['id'])},
                                                    {"$set": {
                                                        "VISITOR_TEAM_ID": team['id']
                                                    }})
