import prepare_db
from pymongo import MongoClient

client = MongoClient()
db = client.nba

ap = prepare_db.player_avg_pts(db.model)
ap.calc_avg_pts()
