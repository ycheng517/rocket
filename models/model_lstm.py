import pymongo
import numpy
from sklearn.metrics import mean_squared_error, r2_score
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import StandardScaler
import pprint

client = pymongo.MongoClient("52.41.48.61", 27017)
db = client.nba_stats

allData = []
all_data_x = []
all_data_y = []

all_players = []

all_players = db.basic_model.distinct("PLAYER_ID")
all_seasons = db.basic_model.distinct("SEASON_ID")

print_count = 0
verification = {}
data = []
count = 0
for season in all_seasons:
    verification[season] = {}
    for player in all_players:
        results = db.basic_model.find({"PLAYER_ID": player,
                                       "SEASON_ID": season}).sort("GAME_DATE", pymongo.ASCENDING)
        count += 1
        print count
        game_count = 0
        season_log = []
        season_log_data = []
        for result in results:
            game_count += 1
            season_log.append(result)
            season_log_data.append([
                result['GAME_PTS'],
                result['GAME_FG3M'],
                result['GAME_FG3A'],
                result['GAME_FGM'],
                result['GAME_FGA'],
                result['GAME_FTM'],
                result['GAME_FTA'],
                result['AVG_PTS']
                ])
        if game_count >= 80:
            verification[season][player] = season_log
            data.append(season_log_data[0:80])
pprint.pprint(data)

dataX = []
dataY = []
look_back = 5
for player_season in data:
    for i in range(len(player_season)-look_back-1):
        x = player_season[i:(i+look_back)]
        y = player_season[i+look_back][0]
        dataX.append(x)
        dataY.append(y)
        
pprint.pprint(dataX)
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
pprint.pprint(dataY)
X = numpy.array(dataX)
y = numpy.array(dataY)
print X.shape
print y.shape

n_train = 2500
X_train = X[:n_train]
y_train = y[:n_train]
X_test = X[n_train:]
y_test = y[n_train:]
idx = numpy.arange(n_train)
numpy.random.seed(13)
numpy.random.shuffle(idx)
X_train = X_train[idx]
y_train = y_train[idx]

model = Sequential()
model.add(LSTM(4, input_shape=(5, 8), activation='linear'))
model.add(Dense(1, activation='linear'))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(X_train, y_train, nb_epoch=100, batch_size=1, verbose=2)

y_test_est = model.predict(X_test)
print("LSTM MSE; %f" % mean_squared_error(y_test, y_test_est))
print("LSTM score: %f" % r2_score(y_test, y_test_est))

