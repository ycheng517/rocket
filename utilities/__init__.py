from nba_py import team as nba_py_team

def create_team_id_dict():
    team_list = nba_py_team.TeamList().info()
    team_id_dict = {}
    for team_item in team_list:
        team_id_dict[team_item['ABBREVIATION']] = team_item
    return team_id_dict

def season_to_season_id(season):
    return "2" + season[0:4]