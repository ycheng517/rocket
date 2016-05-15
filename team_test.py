from nba_py import team
from nba_py import game
from nba_py.player import get_player
from nba_py.constants import *

#------------------------------------------------------------------------------ 
#----------------------- ap = team.TeamGeneralSplits(team_id=TEAMS['ATL']['id'])
#------------------------------------------------------- results = ap.location()
#---------------------------------------------------------------- print(results)
#------------------------------------------------- print(results.columns.values)

#----------------------------- ap = team.TeamSeasons(team_id=TEAMS['ATL']['id'])
#-------------------------------------------------------------- print(ap.info())

ap = game.Boxscore(game_id="0021401184")
print(ap.game_summary())

#----------------------------- ap = team.TeamSummary(team_id=TEAMS['ATL']['id'])
#-------------------------------------------------------------- print(ap.info())
#------------------------------------------------------ print(ap.season_ranks())

#ap = team.TeamLineups(team_id=TEAMS['CLE']['id'], game_id="0021400964", season="2014-15")
#===============================================================================
# print(ap.overall())
# print("=========================================")
# print(ap.lineups())
#===============================================================================
#print(team._api_scrape(ap.json, 1))

#------------------------------------------------------------------------------ 
#------------------------ ap = team.TeamCommonRoster(team_id=TEAMS['CLE']['id'])
#------------------------------------------------------------ print(ap.roster())

#map reduce example: 
