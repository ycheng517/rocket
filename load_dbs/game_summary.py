from nba_py import game
from pymongo import MongoClient

seasons = ['2013-14', '2014-15', '2015-16']

client = MongoClient()
db = client.nba_stats

game_ids = db.game_stats.distinct("GAME_ID")

count = 0
for game_id in game_ids:
    count += 1
    print count
    game_summary = game.Boxscore(str(game_id)).game_summary()
    print game_summary
    db.game_summary.insert_many(game_summary)
