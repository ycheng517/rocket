from nba_py import team
from nba_py.player import get_player
from nba_py.constants import *





ap = team.TeamGeneralSplits(team_id=TEAMS['ATL']['id'], measure_type=MeasureType.Opponent)
print(ap.overall())
print(ap.overall().columns.values)
