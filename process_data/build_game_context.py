import pprint
from nba_py.constants import TEAMS
from utilities import season_to_season_short, game_date_to_python_datetime


class GameContext(object):

    def __init__(self, db, seasons):
        self.db = db
        self.seasons = seasons
        # self.build_win_pct_at_time()
        self.calculate_days_rest()

    def build_win_pct_at_time(self):
        for team in TEAMS.itervalues():
            team_id = team['id']
            for season in self.seasons:
                team_season_game_summaries = self.db.all_games_summaries.find({"SEASON": season_to_season_short(season),
                                                                               "$or": [{"HOME_TEAM_ID": team_id},
                                                                                       {"VISITOR_TEAM_ID": team_id}]})
                if team['name'] in ('Celtics', 'Pacers') and season == '2012-13':
                    assert (team_season_game_summaries.count() == 81), \
                        "actual games played: %s" % team_season_game_summaries.count()
                else:
                    assert(team_season_game_summaries.count() in (82, 66)), \
                        "actual games played: %s" % team_season_game_summaries.count()  #66 games played in lockout seaon

                team_record_list = [dict() for x in range(team_season_game_summaries.count())]
                for game_summary in team_season_game_summaries:
                    game_log = self.db.team_game_logs.find_one({"Game_ID": game_summary['GAME_ID'],
                                                                "TEAM_ID": team_id})
                    if team_id == game_summary['HOME_TEAM_ID']:
                        game_number_to_use = game_summary['HOME_TEAM_GAME_NUMBER']
                        team_record_list[game_number_to_use]['HOME_OR_VISITOR'] = 'HOME'
                    else:
                        game_number_to_use = game_summary['VISITOR_TEAM_GAME_NUMBER']
                        team_record_list[game_number_to_use]['HOME_OR_VISITOR'] = 'VISITOR'
                    team_record_list[game_number_to_use]['RESULT'] = 1 if game_log['WL'] == "W" else 0
                for i in range(len(team_record_list)):
                    if i == 0:
                        team_record_list[i]['WIN_PCT'] = float(team_record_list[i]['RESULT'])
                    else:
                        team_record_list[i]['RESULT'] += team_record_list[i-1]['RESULT']
                        team_record_list[i]['WIN_PCT'] = float(team_record_list[i]['RESULT']) / (i+1)
                    if team_record_list[i]['HOME_OR_VISITOR'] == 'HOME':
                        win_pct_field_name = 'HOME_TEAM_WIN_PCT'
                        team_id_field_name = 'HOME_TEAM_ID'
                        game_number_field_name = 'HOME_TEAM_GAME_NUMBER'
                    else:
                        win_pct_field_name = 'VISITOR_TEAM_WIN_PCT'
                        team_id_field_name = 'VISITOR_TEAM_ID'
                        game_number_field_name = 'VISITOR_TEAM_GAME_NUMBER'
                    result = self.db.all_games_summaries.update_one({"SEASON": season_to_season_short(season),
                                                                     team_id_field_name: team_id,
                                                                     game_number_field_name: i},
                                                                    {"$set": {win_pct_field_name: team_record_list[i]['WIN_PCT']}})
                    assert result.matched_count == 1, \
                        "updated {} results when only 1 should be updated".format(result.matched_count)
                print("updating team win percentages for {} {}:".format(season, team['name']))
                # pprint.pprint(team_record_list)

    def calculate_days_rest(self):
        for team in TEAMS.itervalues():
            team_id = team['id']
            for season in self.seasons:
                print("calculating days rest for {} {}:".format(season, team['name']))
                summaries = self.db.all_games_summaries.find({"SEASON": season_to_season_short(season),
                                                              "$or": [{"HOME_TEAM_ID": team_id},
                                                                      {"VISITOR_TEAM_ID": team_id}]})
                game_dates = []
                for game_summary in summaries:
                    game_time = game_date_to_python_datetime(game_summary['GAME_DATE_EST'])

                    is_home = True if game_summary['HOME_TEAM_ID'] == team_id else False
                    game_dates.append({"game_time": game_time,
                                       "is_home": is_home})

                days_rest = sorted(game_dates, key=lambda k: k['game_time'])

                for i in range(len(days_rest)):
                    if i == 0:
                        # assume 7 days of rest for the first game of the season
                        days_rest[0]['days_rest'] = 7
                    else:
                        days_rest[i]['days_rest'] = (days_rest[i]['game_time'] - days_rest[i-1]['game_time']).days

                    if days_rest[i]['is_home']:
                        game_number_to_use = 'HOME_TEAM_GAME_NUMBER'
                        team_id_field_name = 'HOME_TEAM_ID'
                        days_rest_field_name = 'HOME_TEAM_DAYS_REST'
                    else:
                        game_number_to_use = 'VISITOR_TEAM_GAME_NUMBER'
                        team_id_field_name = 'VISITOR_TEAM_ID'
                        days_rest_field_name = 'VISITOR_TEAM_DAYS_REST'

                    self.db.all_games_summaries.update_one({"SEASON": season_to_season_short(season),
                                                            team_id_field_name: team_id,
                                                            game_number_to_use: i},
                                                           {"$set": {
                                                               days_rest_field_name: days_rest[i]['days_rest']}
                                                           })




