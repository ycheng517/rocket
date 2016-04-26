from prepare_db import player_avg_pts
from prepare_db import player_last_n
from retrieve_db import game_logs
from retrieve_db import team_logs
from pymongo import MongoClient
import sys

assert str(sys.argv[1]) is not None
client = MongoClient(str(sys.argv[1]))
db = client.nba_py

#===============================================================================
# ap = team_logs.TeamLogs(db.team_logs)
#===============================================================================

#===============================================================================
# ap = game_logs.GameLogs(db.game_logs)
#===============================================================================

#===============================================================================
# db.model.remove({})
# cursor = db.game_logs.find().batch_size(25)
# for document in cursor:
#     db.model.insert(document)
#===============================================================================

#===============================================================================
#ap = player_avg_pts.PlayerAvgPts(db.model)
#ap.calc_avg_pts()
#===============================================================================

ap = player_last_n.PlayerLastN(db.model)
ap.calc_last_N()

ap = player_last_n.PlayerLastN(db.model)
ap.calc_last_N(prior_days=7, lastN=1)
