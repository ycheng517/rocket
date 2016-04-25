from prepare_db import player_avg_pts
from retrieve_db import game_logs
from retrieve_db import team_logs
from pymongo import MongoClient

client = MongoClient('52.34.90.220')
db = client.nba_py

#===============================================================================
# ap = team_logs.TeamLogs(db.team_logs)
#===============================================================================

#===============================================================================
# ap = game_logs.GameLogs(db.game_logs)
#===============================================================================

db.model.remove({})
cursor = db.game_logs.find().batch_size(25)
for document in cursor:
    db.model.insert(document)

#===============================================================================
# ap = player_avg_pts.PlayerAvgPts(db.model)
# ap.calc_avg_pts()
#===============================================================================
