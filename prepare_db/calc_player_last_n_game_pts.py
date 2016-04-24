from __future__ import print_function
from nba_py import league
from pymongo import MongoClient
from datetime import datetime, timedelta

client = MongoClient()
db = client.nba_py

logs = db.model.find().batch_size(50)
count = 0
for log in logs: 
    #===========================================================================
    # print("===========================================================")
    # print('player ID: %d, date: %s' % (log['PLAYER_ID'], log['GAME_DATE']))
    #===========================================================================
    time_2_weeks_prior = datetime.strptime(log['GAME_DATE'], '%Y-%m-%d') \
        - timedelta(days=14)
    time_2_weeks_prior = time_2_weeks_prior.strftime("%Y-%m-%d")
    games_last_5 = db.model.aggregate([
        {"$match": {
            "GAME_DATE": {
                "$lte": log['GAME_DATE'], 
                "gt": time_2_weeks_prior
            }, 
            "PLAYER_ID": log['PLAYER_ID'], 
            "SEASON_ID": log['SEASON_ID']
            }
        }, 
        {"$sort": {"GAME_DATE": -1}},
        {"$limit": 5},
        {
            "$group": {
                "_id": {
                    "PLAYER_ID": "$PLAYER_ID", 
                    "SEASON_ID": "$SEASON_ID"
                },
                "AVG_PTS_LAST_5": {"$avg": "$PTS"}
            }
        }
    ])
    for document in games_last_5:
        db.model.update_one(
            {
                "_id": log['_id']
             },
            {
                "$set": {
                     "AVG_PTS_LAST_5": document['AVG_PTS_LAST_5']
                 }
             }, 
            upsert=True
        )
        #=======get last game============
    games_last_1 = db.model.aggregate([
        {"$match": {
            "GAME_DATE": {
                "$lte": log['GAME_DATE'], 
                "gt": time_2_weeks_prior
            }, 
            "PLAYER_ID": log['PLAYER_ID'], 
            "SEASON_ID": log['SEASON_ID']
            }
        }, 
        {"$sort": {"GAME_DATE": -1}},
        {"$limit": 1},
        {
            "$group": {
                "_id": {
                    "PLAYER_ID": "$PLAYER_ID", 
                    "SEASON_ID": "$SEASON_ID"
                },
                #technically shouldn't do this since there's only 1 number to average
                "PTS_LAST_GAME": {"$avg": "$PTS"}
            }
        }
    ])
    for document in games_last_1:
        db.model.update_one(
            {
                "_id": log['_id']
             },
            {
                "$set": {
                     "PTS_LAST_GAME": document['PTS_LAST_GAME']
                 }
             }, 
            upsert=True
        )
    #FOR VERIFICATION
    #===========================================================================
    # games_last_5 = db.model.aggregate([
    #     {"$match": {
    #         "GAME_DATE": {
    #             "$lt": log['GAME_DATE']
    #         }, 
    #         "PLAYER_ID": log['PLAYER_ID'], 
    #         "SEASON_ID": log['SEASON_ID']
    #         }
    #     }, 
    #     {"$sort": {"GAME_DATE": -1}},
    #     {"$limit": 5},
    #     {
    #         "$group": {
    #             "_id": {
    #                 "PLAYER_ID": "$PLAYER_ID",
    #                 "SEASON_ID": "$SEASON_ID",
    #                 "GAME_DATE": "$GAME_DATE", 
    #                 "PTS": "$PTS"
    #             }
    #         }
    #     }
    # ])
    # for document in games_last_5:
    #     print(document)
    #===========================================================================
    count += 1
    print(count)
    