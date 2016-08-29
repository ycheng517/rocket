from nba_py import game
from pymongo import MongoClient, DESCENDING

seasons = ['2013-14', '2014-15', '2015-16']

client = MongoClient()
db = client.nba_stats

games = db.game_summary.find()


for game in games:
    print game['GAME_ID']
    home_game_logs = db.game_stats.find({'GAME_ID': game['GAME_ID'],
                        "TEAM_ID": str(game['HOME_TEAM_ID'])}).sort("MIN", DESCENDING)
    visitor_game_logs = db.game_stats.find({'GAME_ID': game['GAME_ID'],
                        "TEAM_ID": str(game['VISITOR_TEAM_ID'])}).sort("MIN", DESCENDING)
    home_team_stats = db.team_stats.find_one({"TEAM_ID": (game["HOME_TEAM_ID"])})
    del home_team_stats['_id']
    home_team_opp_stats = db.team_opponent_stats.find_one({"TEAM_ID": (game["HOME_TEAM_ID"])})
    del home_team_opp_stats['_id']
    visitor_team_stats = db.team_stats.find_one({"TEAM_ID": (game["VISITOR_TEAM_ID"])})
    del visitor_team_stats['_id']
    visitor_team_opp_stats = db.team_opponent_stats.find_one({"TEAM_ID": (game["VISITOR_TEAM_ID"])})
    del visitor_team_opp_stats['_id']
    # calculate the top 8 players in minutes played
    for home_log in home_game_logs:
        del home_log['_id']
        db.basic_model.insert_one(home_log)
        db.basic_model.update_one(home_log, {"$set": home_team_stats})
        db.basic_model.update_one(home_log, {"$set": visitor_team_opp_stats})
    for visitor_log in visitor_game_logs:
        del visitor_log['_id']
        db.basic_model.insert_one(visitor_log)
        db.basic_model.update_one(visitor_log, {"$set": visitor_team_stats})
        db.basic_model.update_one(visitor_log, {"$set": home_team_opp_stats})
