import time
from datetime import datetime
from nba_py import team as nba_py_team

def create_team_id_dict():
    team_list = nba_py_team.TeamList().info()
    team_id_dict = {}
    for team_item in team_list:
        team_id_dict[team_item['ABBREVIATION']] = team_item
    return team_id_dict

def season_to_season_id(season):
    return "2" + season[0:4]

def season_to_season_short(season):
    return season[:4]

def season_id_to_season(season_id):
    return season_id[1:5]+str(int(season_id[1:5])+1)

def game_date_to_python_time(game_date):
    return time.strptime(game_date, "%Y-%m-%dT%H:%M:%S")

def game_date_to_python_datetime(game_date):
    return datetime.strptime(game_date, "%Y-%m-%dT%H:%M:%S")
