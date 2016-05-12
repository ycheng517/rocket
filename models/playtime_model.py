import sys
import numpy as np
from pymongo import MongoClient
from sklearn import linear_model, preprocessing
import matplotlib.pyplot as plt


assert str(sys.argv[1]) is not None
client = MongoClient(str(sys.argv[1]))
db = client.nba_py

cursor = db.playtime_model.find({"PLAYER_ID": 203521, "SEASON_ID": "22015"})

allData = []
allDataX = []
allDataY = []

roster = db.rosters.find_one({"TEAM_ABBREVIATION": "CLE", 
                                     "SEASON_ID": "22015"})
variables = []
for player in roster['roster']: 
    games_played = db.playtime_model.find({"PLAYER_ID": int(player), "SEASON_ID": "22015", "MIN": {"$gt": 0}}).count()
    avg_min = db.playtime_model.find_one({"PLAYER_ID": int(player), "SEASON_ID": "22015"})['AVG_MIN']
    if games_played > 30 and avg_min > 15 and int(player) != 203521: 
        variables.append(player)
#-------------------------------------------------- variables = roster['roster']
print("total number of players on the roster: %d" % len(roster['roster']))
print("total number of players considered: %d" % len(variables))
print(variables)

variables = ['202681', '202697', '2210', '2590', '2747']
avg_min = db.playtime_model.find_one({"PLAYER_ID": 203521, "SEASON_ID": "22015"})['AVG_MIN']
print("avg min: %d" % avg_min)
count = 0
for document in cursor:
    dataRow = []
    for variable in variables:
        dataRow.append(document['lineup'][variable])
    dataRow.append(document['MIN'])
    allData.append(dataRow)
    count = count + 1
print("game count: %d" % count)
Xy = np.array(allData)
np.random.shuffle(Xy)
X = Xy[:, range(0, Xy.shape[1]-1) ]
y = Xy[:, Xy.shape[1]-1]
#--------------------------------------------------------------------- print(Xy)
#---------------------------------------------------------------------- print(X)
#---------------------------------------------------------------------- print(y)
X_normalized = (X)


# X_normalized = np.ones((X_normalized_no_ones.shape[0], X_normalized_no_ones.shape[1]+1))
#------------------------------------ X_normalized[:, 1:] = X_normalized_no_ones

# Separate into Train and Test datasets
train_test_split = int(round(len(y) * 0.7))
X_normalized_train = X_normalized[:train_test_split]
X_normalized_test = X_normalized[train_test_split:]
y_train = y[:train_test_split]
y_test = y[train_test_split:]

# train model
regr = linear_model.Ridge(alpha=1, fit_intercept=True)
regr.fit(X_normalized_train, y_train)

# The coefficients
print('Coefficients: \n', regr.coef_)
print('Intercepts: \n', regr.intercept_)
for i in range(0, regr.coef_.size):
    print (variables[i], regr.coef_[i])
print("================")
print(variables)
print(regr.coef_)
# The mean square error
print("Residual sum of squares for training set: %.2f"
      % np.mean((regr.predict(X_normalized_train) - y_train) ** 2))
print('Variance score: %.2f' % regr.score(X_normalized_train, y_train))
print("Residual sum of squares for test set: %.2f"
      % np.mean((regr.predict(X_normalized_test) - y_test) ** 2))
print('Variance score: %.2f' % regr.score(X_normalized_test, y_test))

#~~~~calculate against baseline~~~~~~~~~~~

cursor = db.playtime_model.find({"PLAYER_ID": 203521, "SEASON_ID": "22015"})
count = 0
dumb_y_list = []
for document in cursor:
    if document['MIN'] > 10:
        dumb_y_list.append(document['MIN'])
        count = count + 1
print("dumb model count: %d" % count)

dumb_X = avg_min * np.ones((len(dumb_y_list), 1))
dumb_y = np.array(dumb_y_list)
#----------------------------------------------------------------- print(dumb_X)
#----------------------------------------------------------------- print(dumb_y)
# compare against dumb model which is just the ppg average
print('dumb average RSS: %.2f' % np.mean((dumb_X - dumb_y) ** 2))
dumb_regr = linear_model.LinearRegression(fit_intercept=True)
dumb_regr.fit(dumb_X, dumb_y)
print('dumb average Variance score: %.2f' % dumb_regr.score(dumb_X, dumb_y))

#===============plotting===================
plt.scatter(X_normalized_test[:,0], y_test,  color='black')
predicted_y = X_normalized_test[:,0] * regr.coef_[0] + regr.intercept_
plt.plot(X_normalized_test[:,0], predicted_y, color='blue',
         linewidth=3)

plt.xticks(())
plt.yticks(())

plt.show()


