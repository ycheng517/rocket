'''
Add the game number (1-82) to each game played, this is crucial for doing later analysis
'''

from nba_py.constants import TEAMS
from utilities import season_to_season_short
import time


class GameNumber(object):
    def __init__(self, db, seasons):
        self.db = db
        self.seasons = seasons
        self.add_game_number_to_game_summary()

    def add_game_number_to_game_summary(self):
        if self.db.game_number_lookup.count({"GAME_NUMBER":{ "$exists": False}}) == 0 and \
            self.db.game_number_lookup.count() == self.db.all_games_summaries.count() * 2:
            print ("game number lookup collection already exists, skipping")
            return
        self.db.game_number_lookup.drop()
        for team in TEAMS.itervalues():
            for season in self.seasons:
                print("building game number lookup for {} {}".format(season, team['name']))
                team_id = team['id']
                games_this_season = self.db.all_games_summaries.find({"$or": [{"HOME_TEAM_ID": int(team_id)},
                                                                           {"VISITOR_TEAM_ID": int(team_id)}],
                                                                   "SEASON": season_to_season_short(season)})
                if (team['name'] in ('Celtics', 'Pacers') and season == '2012-13'):
                    assert (games_this_season.count() == 81), \
                    "actual games played: %s" % games_this_season.count()
                else:
                    assert(games_this_season.count() in (82, 66)), \
                    "actual games played: %s" % games_this_season.count()  #66 games played in  lockout seaon
                games_this_season_list = []
                for game in games_this_season:
                    # example: 2008-03-28T00:00:00
                    game['python_time'] = time.strptime(game['GAME_DATE_EST'], "%Y-%m-%dT%H:%M:%S")
                    games_this_season_list.append(game)
                games_this_season_list.sort(key=lambda d: d['python_time'])
                for i in range(len(games_this_season_list)):
                    games_this_season_list[i]['GAME_NUMBER'] = i+1
                    games_this_season_list[i]['HOME_TEAM_ID'] = str(games_this_season_list[i]['HOME_TEAM_ID'])
                    games_this_season_list[i]['VISITOR_TEAM_ID'] = str(games_this_season_list[i]['VISITOR_TEAM_ID'])
                    del games_this_season_list[i]['python_time']
                    del games_this_season_list[i]['LIVE_PC_TIME']
                    del games_this_season_list[i]['LIVE_PERIOD_TIME_BCAST']
                    del games_this_season_list[i]['NATL_TV_BROADCASTER_ABBREVIATION']
                    del games_this_season_list[i]['WH_STATUS']
                    del games_this_season_list[i]['_id']
                    del games_this_season_list[i]['GAME_SEQUENCE']
                    del games_this_season_list[i]['GAME_STATUS_ID']
                    del games_this_season_list[i]['GAME_STATUS_TEXT']
                    
                self.db.game_number_lookup.insert_many(games_this_season_list)