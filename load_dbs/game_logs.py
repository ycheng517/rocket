from utilities import season_to_season_id, create_team_id_dict
from nba_py import league


class GameLogs(object):
    def __init__(self, db, seasons, use_team_id):
        self.db = db
        self.seasons = seasons
        self.load_player_game_logs(use_team_id=use_team_id)

    def load_player_game_logs(self, use_team_id=False):
        print("saving player game logs to database")
        print("===================================")
        for season in self.seasons:
            if self.db.game_logs.count({"SEASON_ID": season_to_season_id(season)}) > 0:
                print("season {} of game logs already exists, skipping".format(season))
                continue
            ap = league.GameLog(season=season)
            logs = ap.overall()
            print ("processing season %s with %d entries" % (season, (len(logs))))
            self.db.game_logs.insert_many(logs)
        if use_team_id == True:
            self.insert_team_id()

    def insert_team_id(self):
        print("inserting team id to game logs collection")
        print("===================================")
        team_id_dict = create_team_id_dict()
        for season in self.seasons:
            if self.db.game_logs.count({"SEASON_ID": season_to_season_id(season), "TEAM_ID": {"$exists": True}}) > 0:
                print("TEAM_ID already exists for season {} of team logs, skipping".format(season))
                continue
            team_abbrevs = self.db.game_logs.find({"SEASON_ID": season_to_season_id(season)}).distinct("TEAM_ABBREVIATION")
            for abbrev in team_abbrevs:
                print("inserting team id for team {} in for season {}".format(abbrev, season))
                if abbrev in ('NOK', 'NOH'):
                    team_id = team_id_dict['NOP']['TEAM_ID']
                elif abbrev == 'SEA':
                    team_id = team_id_dict['OKC']['TEAM_ID']
                elif abbrev == 'NJN':
                    team_id = team_id_dict['BKN']['TEAM_ID']
                else:
                    team_id = team_id_dict[abbrev]['TEAM_ID']
                self.db.game_logs.update_many({"TEAM_ABBREVIATION": abbrev},
                                              {'$set':
                                               {"TEAM_ID": int(team_id)}})

