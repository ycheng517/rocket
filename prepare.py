from prepare_db import player_avg_pts
from pymongo import MongoClient

client = MongoClient()
db = client.nba_py

ap = player_avg_pts.PlayerAvgPts(db.model)
ap.calc_avg_pts()
