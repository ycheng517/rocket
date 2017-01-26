'''
Add the game number (1-82) to all_games_summaries,
this is crucial for doing later analysis
'''

from nba_py.constants import TEAMS
from utilities import season_to_season_short, game_date_to_python_time
import time


class GameNumber(object):
    def __init__(self, db, seasons):
        self.db = db
        self.seasons = seasons
        self.add_game_number_to_game_summary()

    def add_game_number_to_game_summary(self):
        if self.db.all_games_summaries.count({"HOME_TEAM_GAME_NUMBER":{ "$exists": False}}) == 0 and \
                self.db.all_games_summaries.count({"VISITOR_TEAM_GAME_NUMBER":{ "$exists": False}}) == 0:
            print ("game number lookup collection already exists, skipping")
            return
        self.db.game_number_lookup.drop()
        for team in TEAMS.itervalues():
            for season in self.seasons:
                print("building game number lookup for {} {}".format(season, team['name']))
                team_id = team['id']
                games_this_season = self.db.all_games_summaries.find({"$or": [{"HOME_TEAM_ID": team_id},
                                                                           {"VISITOR_TEAM_ID": team_id}],
                                                                   "SEASON": season_to_season_short(season)})
                if team['name'] in ('Celtics', 'Pacers') and season == '2012-13':
                    assert (games_this_season.count() == 81), \
                        "actual games played: %s" % games_this_season.count()
                else:
                    assert(games_this_season.count() in (82, 66)), \
                        "actual games played: %s" % games_this_season.count()  #66 games played in  lockout seaon
                games_this_season_list = []
                for game in games_this_season:
                    # example: 2008-03-28T00:00:00
                    game['python_time'] = game_date_to_python_time(game['GAME_DATE_EST'])
                    games_this_season_list.append(game)
                games_this_season_list.sort(key=lambda d: d['python_time'])
                for i in range(len(games_this_season_list)):
                    field_to_update = "HOME_TEAM_GAME_NUMBER" if games_this_season_list[i]['HOME_TEAM_ID'] == team_id \
                        else "VISITOR_TEAM_GAME_NUMBER"
                    self.db.all_games_summaries.update_many(
                        {"GAME_ID": games_this_season_list[i]['GAME_ID']},
                        {"$set": {field_to_update: i}})
