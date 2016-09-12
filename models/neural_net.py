from pymongo import MongoClient
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

client = MongoClient("52.41.48.61", 27017)
db = client.nba_stats

allData = []
all_data_x = []
all_data_y = []


# load data from DB
all_results = db.basic_model.find({})
count = 0
for sample in all_results:
    count+=1
    all_data_x.append([
                    sample['AGE'],
                    sample['AVG_MIN'],
                    sample['AVG_FGA'],
                    sample['AVG_FGM'],
                    sample['AVG_FTA'],
                    sample['AVG_FTM'],
                    sample['AVG_FG3A'],
                    sample['AVG_FG3M'],
                    sample['AVG_PTS'],
                    sample['AVG_PTS'],
                    sample['AVG_PTS'],
                    sample['AVG_REB'],
                    sample['AVG_DREB'],
                    sample['AVG_AST'],
                    sample['AVG_STL'],
                    sample['AVG_BLK'],
                    sample['AVG_BLKA'],
                    sample['AVG_PF'],
                    sample['AVG_PFD'],
                    sample['AVG_TOV'],
                    sample['TEAM_W_PCT'],
                    sample['TEAM_PLUS_MINUS'],
                    sample['TEAM_FGA'],
                    sample['TEAM_FGM'],
                    sample['TEAM_FG3A'],
                    sample['TEAM_FG3M'],
                    sample['TEAM_FTA'],
                    sample['TEAM_FTM'],
                    sample['TEAM_REB'],
                    sample['TEAM_DREB'],
                    sample['TEAM_AST'],
                    sample['TEAM_STL'],
                    sample['TEAM_BLK'],
                    sample['TEAM_BLKA'],
                    sample['TEAM_TOV'],
                    sample['TEAM_PF'],
                    sample['TEAM_PFD'],
                    sample['OPP_W_PCT'],
                    sample['OPP_PLUS_MINUS'],
                    sample['OPP_FGA'],
                    sample['OPP_FGM'],
                    sample['OPP_FG3A'],
                    sample['OPP_FG3M'],
                    sample['OPP_FTA'],
                    sample['OPP_FTM'],
                    sample['OPP_REB'],
                    sample['OPP_DREB'],
                    sample['OPP_AST'],
                    sample['OPP_STL'],
                    sample['OPP_BLK'],
                    sample['OPP_BLKA'],
                    sample['OPP_TOV'],
                    sample['OPP_PF'],
                    sample['OPP_PFD'],
                    ])
    all_data_y.append(sample['GAME_PTS'])

print("total size of dataset is %d" % count)

# generate data set
X = np.array(all_data_x)
y = np.array(all_data_y)

num_features = X.shape[1]
print("num of features: %d" % num_features)

n_train = 30000
X_train = X[:n_train]
y_train = y[:n_train]
X_test = X[n_train:]
y_test = y[n_train:]
idx = np.arange(n_train)
np.random.seed(13)
np.random.shuffle(idx)
X_train = X_train[idx]
y_train = y_train[idx]

# create model
model = Sequential()
model.add(Dense(int(num_features / 2), input_dim=num_features, init='normal', activation='linear'))
model.add(Dense(int(num_features / 4), init='normal', activation='linear'))
model.add(Dense(1, init='normal', activation='linear'))
# Compile model
model.compile(loss='mse', optimizer='rmsprop')
model.fit(X_train, y_train, nb_epoch=50, batch_size=256, verbose=1)
score, acc = model.evaluate(X_test, y_test)

print "~~~~~~~~~~\n"
print score
print acc
