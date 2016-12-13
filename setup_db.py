from pymongo import MongoClient
import sys
from load_dbs import game_logs

assert str(sys.argv[1]) is not None
client = MongoClient(str(sys.argv[1]))
# TODO: have proper argparse for this
db = client.nba_stats

seasons = ['2007-08', '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16']

game_logs.GameLogs(db, seasons, use_team_id=True)