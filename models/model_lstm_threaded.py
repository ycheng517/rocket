import pymongo
import numpy
from sklearn.metrics import mean_squared_error, r2_score
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import StandardScaler
import pprint
import Queue
from threading import Thread

client = pymongo.MongoClient("52.41.48.61", 27017)
db = client.nba_stats

allData = []
all_data_x = []
all_data_y = []

all_players = []

all_players = db.basic_model.distinct("PLAYER_ID")
all_seasons = db.basic_model.distinct("SEASON_ID")


print_count = 0
global verification
verification = {}
global data
data = []
global count
count = 0
unique_entries = []
for season in all_seasons:
    verification[season] = {}
    for player in all_players:
        unique_entries.append({"PLAYER_ID": player,
                               "SEASON_ID": season})
        
        results = db.basic_model.find({"PLAYER_ID": player,
                                       "SEASON_ID": season}).sort("GAME_DATE", pymongo.ASCENDING)

num_worker_threads = 8

def worker():
    global count
    while True:
        item = q.get()
        results = db.basic_model.find(item).sort("GAME_DATE", pymongo.ASCENDING)
        count = count + 1
        print count
        game_count = 0
        sequence_log = []
        sequence_log_data = []
        prev_game_number = 0
        for result in results:
            if result['GAME_NUMBER'] - prev_game_number == 1: 
                game_count += 1
                sequence_log.append(result)
                sequence_log_data.append([
                    result['GAME_PTS'],
                    result['GAME_FG3M'],
                    result['GAME_FG3A'],
                    result['GAME_FGM'],
                    result['GAME_FGA'],
                    result['GAME_FTM'],
                    result['GAME_FTA'],
                    result['AVG_PTS']
                    ])
            else: 
                if len(sequence_log_data) > 10:
                    verification[season][player] = sequence_log
                    data.append(sequence_log_data)
                sequence_log = []
                sequence_log_data = []
            prev_game_number = result['GAME_NUMBER']
        if len(sequence_log_data) > 10:
            verification[season][player] = sequence_log
            data.append(sequence_log_data)

        q.task_done()

q = Queue.Queue()
for i in range(num_worker_threads):
    t = Thread(target=worker)
    t.daemon = True
    t.start()

for item in unique_entries:
    q.put(item)

q.join()       # block until all tasks are done

for season, players in verification.iteritems():
    for player, games in players.iteritems():
        for entry in games:
            print("player: %s, date: %s" % (entry['PLAYER_NAME'], entry['GAME_DATE']))

dataX = []
dataY = []
look_back = 5
for player_season in data:
    for i in range(len(player_season)-look_back-1):
        x = player_season[i:(i+look_back)]
        y = player_season[i+look_back][0]
        dataX.append(x)
        dataY.append(y)
        
#===============================================================================
# pprint.pprint(dataX)
# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
# pprint.pprint(dataY)
#===============================================================================
X = numpy.array(dataX)
y = numpy.array(dataY)
print X.shape
print y.shape

n_train = 12000
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
model.fit(X_train, y_train, nb_epoch=50, batch_size=64, verbose=2)
score = model.evaluate(X_test, y_test, verbose=1)
print "\n"
print score
#===============================================================================
# y_test_est = model.predict(X_test)
# print("LSTM MSE; %f" % mean_squared_error(y_test, y_test_est))
# print("LSTM score: %f" % r2_score(y_test, y_test_est))
#===============================================================================

