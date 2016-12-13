from nba_py import team as nba_py_team
from nba_py.constants import TEAMS
from utilities import season_to_season_id
import pandas
import pprint

class TeamGameLogs(object):
    def __init__(self, db, seasons):
        self.db = db
        self.seasons = seasons
        self.load_team_game_logs()
    
    def load_team_game_logs(self):
        print("saving team game logs to database")
        print("=================================")
        for season in self.seasons:
            for team in TEAMS.itervalues():
                # check if logs already stored
                if self.db.team_game_logs.count({"SEASON_ID": season_to_season_id(season),
                                            "TEAM_ID": team['id']}) > 0:
                    print("team game logs for {} {} already exists, skipping".format(season, team['name']))
                    continue
                print("storing team game logs for {} {}".format(season, team['name']))
                ap = nba_py_team.TeamGameLogs(team_id=team['id'], season=season)
                results = ap.info()
                if isinstance(results, pandas.DataFrame):
                    results = results.to_dict("records")
                for result in results:
                    result['SEASON_ID'] = season_to_season_id(season)
                    result['TEAM_ID'] = str(result['Team_ID'])
                    del result['Team_ID']
                self.db.team_game_logs.insert_many(results)