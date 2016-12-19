from nba_py import game
import pandas
from threading import Thread
from Queue import Queue

seasons = ['2007-08', '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16']


class AllGamesSummaries(object):
    def __init__(self, db):
        self.db = db
        self.get_all_games_summaries()
        self.q = Queue()

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

    def get_all_games_summaries(self):
        # this is a hidden dependency
        #TODO: make team_id a string
        game_ids = self.db.player_game_logs.distinct("GAME_ID")
        if self.db.all_games_summaries.count() == len(game_ids):
            print ("all games summaries already exist, skip processing")
            return

        self.db.all_games_summaries.drop()
        print("gathering game summaries for %d games" % len(game_ids))
        for game_id in game_ids:
            self.q.put(game_id)

        for i in range(8):
            t = Thread(target=self.worker, args=(self.q))
            t.start()

        self.q.join()
