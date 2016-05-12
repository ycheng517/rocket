import sys
import numpy as np
from pymongo import MongoClient
from sklearn import linear_model, preprocessing, cluster
import matplotlib.pyplot as plt

assert str(sys.argv[1]) is not None
client = MongoClient(str(sys.argv[1]))
db = client.nba_py

all_players = db.player_averages.find()

variables = ['FGM', 'FGA',
             'FG3M', 'FG3A',
             'FTM', 'FTA',
             'REB', 'AST',
             'STL', 'BLK',
             'TOV'
             ]
X_list = []
_id_list = []
count = 0
for player in all_players:
    count +=1 
    print(count)
    dataRow = []
    for variable in variables:
        dataRow.append(player[variable])
    X_list.append(dataRow)
    _id_list.append(player['_id'])
    
X = np.array(X_list)
X_normalized = preprocessing.scale(X)
model = cluster.KMeans(n_clusters=20)
results = model.fit_predict(X_normalized)
print(results)

for idx, val in enumerate(_id_list):
    print (idx)
    print (val)
    db.player_averages.update_one({"_id": val}, 
                                   {"$set": {"PLAYER_GROUP": int(results[idx])}})