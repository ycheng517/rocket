from nba_py import team
from nba_py.player import get_player
from nba_py.constants import *




#===============================================================================
# 
# ap = team.TeamGeneralSplits(team_id=TEAMS['ATL']['id'], measure_type=MeasureType.Opponent)
# print(ap.overall())
# print(ap.overall().columns.values)
#===============================================================================

#ap = team.TeamLineups(team_id=TEAMS['CLE']['id'], game_id="0021400964", season="2014-15")
#===============================================================================
# print(ap.overall())
# print("=========================================")
# print(ap.lineups())
#===============================================================================
#print(team._api_scrape(ap.json, 1))


ap = team.TeamCommonRoster(team_id=TEAMS['CLE']['id'])
print(ap.roster())