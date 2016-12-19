from pymongo import MongoClient
import sys
from retrieve_data_from_web import player_game_logs, team_game_logs, player_shooting_splits,\
    game_summary
from process_data import game_number

assert str(sys.argv[1]) is not None
client = MongoClient(str(sys.argv[1]))
# TODO: have proper argparse for this
db = client.nba_stats

seasons = ['2007-08', '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16']
# convesion: team ID is string, game ID is string, use season_id instead of season when possible

########################
# Retrieve Data from Web
########################

# player_game_logs.PlayerGameLogs(db, seasons, use_team_id=True)

# team_game_logs.TeamGameLogs(db, seasons)

# player_shooting_splits.PlayerShootingSplits(db, seasons)

# game_summary.AllGamesSummaries(db)

#############
# Build Model
#############

game_number.GameNumber(db, seasons)