from nba_py import game
from pymongo import MongoClient, DESCENDING

seasons = ['2013-14', '2014-15', '2015-16']

client = MongoClient()
db = client.nba_stats

games = db.game_summary.find()


for game in games:
    home_game_logs = db.game_stats.find({'GAME_ID': game['GAME_ID'],
                        "TEAM_ID": game['HOME_TEAM_ID']}).sort("MIN", DESCENDING)
    
    visitor_game_logs = db.game_stats.find({'GAME_ID': game['GAME_ID'],
                        "TEAM_ID": game['VISITOR_TEAM_ID']}).sort("MIN", DESCENDING)
    # calculate the top 8 players in minutes played

