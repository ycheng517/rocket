from utilities import season_to_season_id
from nba_py import league
import pandas


class PlayerGameLogs(object):
    def __init__(self, db, seasons, use_team_id):
        self.db = db
        self.seasons = seasons
        self.load_player_game_logs(use_team_id=use_team_id)

    def load_player_game_logs(self, use_team_id=False):
        print("saving player game logs to database")
        print("===================================")
        for season in self.seasons:
            if self.db.player_game_logs.count({"SEASON_ID": season_to_season_id(season)}) > 0:
                print("season {} of game logs already exists, skipping".format(season))
                continue
            ap = league.GameLog(season=season)
            logs = ap.overall()
            if isinstance(logs, pandas.DataFrame):
                logs = logs.to_dict("records")
            print ("processing season %s with %d entries" % (season, (len(logs))))
            for log in logs:
                log['TEAM_ID'] = str(log['TEAM_ID'])
                log['PLAYER_ID'] = str(log['PLAYER_ID'])
            self.db.player_game_logs.insert_many(logs)