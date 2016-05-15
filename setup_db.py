from prepare_db import player_avg_pts
from prepare_db import player_last_n
from prepare_db import lineups
from retrieve_db import game_logs, team_opp_logs
from retrieve_db import team_logs
from retrieve_db import team_opp_logs
from retrieve_db import player_averages
from retrieve_db import team_stats
from prepare_db import prepare_playtime_clustered_model
from prepare_db import player_avg_stats
from pymongo import MongoClient
import sys
from models import prepare_playtime_model

assert str(sys.argv[1]) is not None
client = MongoClient(str(sys.argv[1]))
db = client.nba_py



#~~~~~~~~~~~~~Prepare DB~~~~~~~~~~~~~~~~~
#===============================================================================
# ap = team_logs.TeamLogs(db.team_logs)
#===============================================================================

#----------------------------------------- ap = game_logs.GameLogs(db.game_logs)
#------------------------------------------------- ap.add_team_ids(db.team_logs)

#===============================================================================
# ap = team_opp_logs.TeamOppLogs(db.team_opp_logs)
#===============================================================================

#ap = player_averages.PlayerAverages(db.player_averages)

#-------------------------------------- ap = team_stats.TeamStats(db.team_stats)

#~~~~~~~~~~~~Copy DB to model~~~~~~~~~~~~~
#===============================================================================
# db.model.remove({})
# cursor = db.game_logs.find().batch_size(25)
# for document in cursor:
#     db.model.insert(document)
#===============================================================================


#~~~~~~~~~~~~PPM Calculations~~~~~~~~~~~
#===============================================================================
#ap = player_avg_pts.PlayerAvgPts(db.model)
#ap.calc_avg_pts()
#===============================================================================

#===============================================================================
# ap = player_last_n.PlayerLastN(db.model)
# ap.calc_last_N()
# 
# ap = player_last_n.PlayerLastN(db.model)
# ap.calc_last_N(prior_days=7, lastN=1)
#===============================================================================

# ap = player_avg_stats.PlayerAvgStats(db.player_averages) ---------------------
# ap.calc_avg_stats(db.game_logs) ----------------------------------------------


#~~~~~~~~~~~~MPG Calculations~~~~~~~~~~~~~
#------------------------------------- ap = lineups.GameLineups(db.game_lineups)
#---------- ap.calc_game_lineups(game_logs=db.game_logs, team_logs=db.team_logs)

# ap = prepare_playtime_clustered_model.PlaytimeModel(db.playtime_model_clustered)
#--- ap.load_minutes(game_logs=db.game_logs, player_averages=db.player_averages)
# ap.load_lineups(game_lineups=db.game_lineups, player_averages=db.player_averages)

ap = prepare_playtime_clustered_model.PlaytimeModel(db.playtime_model)
ap.empty_collection()
ap.load_minutes(game_logs=db.game_logs, player_averages=db.player_averages)
ap.load_lineups(game_lineups=db.game_lineups, player_averages=db.player_averages)
ap.load_avg_stats(player_averages = db.player_averages)
ap.load_team_records(db.game_logs, db.team_stats)


