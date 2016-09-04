import pprint
from pymongo import MongoClient
import numpy as np
from keras.models import Sequential
from sklearn.metrics import mean_squared_error

seasons = ['2013-14', '2014-15', '2015-16']

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
    all_data_x.append([sample['AGE'],
                     sample['AVG_MIN'],
                     sample['AVG_FGA'],
                     sample['AVG_FGM'],
                     sample['AVG_FTA'],
                     sample['AVG_FTM'],
                     sample['AVG_FG3A'],
                     sample['AVG_FG3M'],
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
                     sample['OPP_PFD']
                     ])
    all_data_y.append(sample['GAME_PTS'])

print("total size of dataset is %d" % count)


# example validation
sample = db.basic_model.find_one({"PLAYER_NAME": "Kyrie Irving"})
carmelo_X = [sample['AGE'],
             sample['AVG_MIN'],
             sample['AVG_FGA'],
             sample['AVG_FGM'],
             sample['AVG_FTA'],
             sample['AVG_FTM'],
             sample['AVG_FG3A'],
             sample['AVG_FG3M'],
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
             sample['OPP_PFD']
             ]
carmelo_y = sample['GAME_PTS']


# generate data set
all_data_x = np.array(all_data_x)
all_data_y = np.array(all_data_y)

n_train = 35000
X_train = all_data_x[:n_train]
y_train = all_data_y[:n_train]
X_test = all_data_x[n_train:]
y_test = all_data_y[n_train:]
idx = np.arange(n_train)
np.random.seed(13)
np.random.shuffle(idx)
X_train = X_train[idx]
y_train = y_train[idx]

std = X_train.std(axis=0)
mean = X_train.mean(axis=0)
X_train = (X_train - mean) / std
X_test = (X_test - mean) / std
carmelo_X = (carmelo_X - mean) / std

std = y_train.std(axis=0)
mean = y_train.mean(axis=0)
y_train = (y_train - mean) / std
y_test = (y_test - mean) / std
carmelo_y = (carmelo_y - mean) / std

#train neural net
print("training neural net\n=============")
model = Sequential()


from keras.layers import Dense, Activation

model.add(Dense(output_dim=25, input_dim=52))
model.add(Activation("relu"))
model.add(Dense(output_dim=1))


model.compile(loss='mean_squared_error', optimizer='sgd')

model.fit(X_train, y_train, nb_epoch=50, batch_size=50)
y_test_est = model.predict(X_test, batch_size=50, verbose=1)
print("\nlinear regression MSE; %f" % mean_squared_error(y_test, y_test_est))


# #------------- loss_and_metrics = model.evaluate(X_test, y_test, batch_size=100)
#--------------------- print("\nprinting loss and metrics\n===================")
#------------------------------------------------------- print(loss_and_metrics)
