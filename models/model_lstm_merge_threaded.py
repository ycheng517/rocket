import pymongo
import numpy
from sklearn.metrics import mean_squared_error, r2_score
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM, Merge
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
        sequence_log_data_aux = []
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
                    ])
                sequence_log_data_aux.append([
                    result['AVG_PTS'],
                    result['AGE'],
                    result['AVG_MIN'],
                    result['AVG_REB'],
                    result['AVG_DREB'],
                    result['AVG_AST'],
                    result['AVG_STL'],
                    result['AVG_BLK'],
                    result['AVG_BLKA'],
                    result['AVG_PF'],
                    result['AVG_PFD'],
                    result['AVG_TOV'],
                    result['TEAM_W_PCT'],
                    result['TEAM_PLUS_MINUS'],
                    result['TEAM_FGA'],
                    result['TEAM_FGM'],
                    result['TEAM_FG3A'],
                    result['TEAM_FG3M'],
                    result['TEAM_FTA'],
                    result['TEAM_FTM'],
                    result['TEAM_REB'],
                    result['TEAM_DREB'],
                    result['TEAM_AST'],
                    result['TEAM_STL'],
                    result['TEAM_BLK'],
                    result['TEAM_BLKA'],
                    result['TEAM_TOV'],
                    result['TEAM_PF'],
                    result['TEAM_PFD'],
                    result['OPP_W_PCT'],
                    result['OPP_PLUS_MINUS'],
                    result['OPP_FGA'],
                    result['OPP_FGM'],
                    result['OPP_FG3A'],
                    result['OPP_FG3M'],
                    result['OPP_FTA'],
                    result['OPP_FTM'],
                    result['OPP_REB'],
                    result['OPP_DREB'],
                    result['OPP_AST'],
                    result['OPP_STL'],
                    result['OPP_BLK'],
                    result['OPP_BLKA'],
                    result['OPP_TOV'],
                    result['OPP_PF'],
                    result['OPP_PFD'],
                    ])
            else: 
                if len(sequence_log_data) > 10:
                    verification[season][player] = sequence_log
                    data.append({'sequence_log_data': sequence_log_data,
                                 'sequence_log_data_aux': sequence_log_data_aux})
                sequence_log = []
                sequence_log_data = []
                sequence_log_data_aux = []
            prev_game_number = result['GAME_NUMBER']
        if len(sequence_log_data) > 10:
            verification[season][player] = sequence_log
            data.append({'sequence_log_data': sequence_log_data,
                                 'sequence_log_data_aux': sequence_log_data_aux})

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
dataX_aux = []
# reformat data for look back
look_back = 5
for player_season in data:
    for i in range(len(player_season['sequence_log_data'])-look_back-1):
        x = player_season['sequence_log_data'][i:(i+look_back)]
        y = player_season['sequence_log_data'][i+look_back][0]
        aux = player_season['sequence_log_data_aux'][i]
        dataX.append(x)
        dataY.append(y)
        dataX_aux.append(aux)


print "~~~~~~~~~~~~~~~~dataX~~~~~~~~~~~~~~~~~"
pprint.pprint(dataX[0:5])
pprint.pformat(dataX)
print "~~~~~~~~~~~~~~~dataX_aux~~~~~~~~~~~~~~~~~~"
pprint.pprint(dataX_aux[0:5])
pprint.pformat(dataX_aux)
print "~~~~~~~~~~~~~~~dataY~~~~~~~~~~~~~~~~~~"
pprint.pprint(dataY[0:5])
pprint.pformat(dataY)

X = numpy.array(dataX)
y = numpy.array(dataY)
X_aux = numpy.array(dataX_aux)
print X.shape
print y.shape
print X_aux.shape

n_train = 12000
X_train = X[:n_train]
X_aux_train = X_aux[:n_train]
y_train = y[:n_train]
X_test = X[n_train:]
X_aux_test = X_aux[n_train:]
y_test = y[n_train:]
idx = numpy.arange(n_train)
numpy.random.seed(13)
numpy.random.shuffle(idx)
X_train = X_train[idx]
X_aux_train = X_aux_train[idx]
y_train = y_train[idx]

# training neural net
model_lstm = Sequential()
model_lstm.add(LSTM(4, input_shape=(5, 7), activation='linear'))
model_lstm.add(Dense(1, activation='linear'))

aux_features = X_aux.shape[1]
model_aux = Sequential()
model_aux.add(Dense(aux_features, input_dim=aux_features, activation='linear'))

merged = Merge([model_lstm, model_aux], mode='concat')

final_model = Sequential()
final_model.add(merged)
final_model.add(Dense(26, activation='linear'))
final_model.add(Dense(13, activation='linear'))
final_model.add(Dense(1, activation='linear'))
final_model.compile(loss='mean_squared_error', optimizer='adam')

final_model.fit([X_train, X_aux_train], y_train, nb_epoch=50, batch_size=64, verbose=2)
score = final_model.evaluate([X_test, X_aux_test], y_test, verbose=1)
print "\n"
print score
y_test_est = final_model.predict([X_test, X_aux_test])
print("LSTM MSE; %f" % mean_squared_error(y_test, y_test_est))
print("LSTM score: %f" % r2_score(y_test, y_test_est))


