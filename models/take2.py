import pprint
from pymongo import MongoClient
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import r2_score, mean_squared_error

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
                    sample['AVG_REB'],
                    sample['AVG_DREB'],
                    sample['AVG_AST'],
                    sample['AVG_STL'],
                    sample['AVG_BLK'],
                    sample['AVG_BLKA'],
                    sample['AVG_PF'],
                    sample['AVG_PFD'],
                    sample['AVG_TOV'],
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
    all_data_y.append(sample['GAME_PTS'] / sample['GAME_MIN'])

print("total size of dataset is %d" % count)


# generate data set
all_data_x = np.array(all_data_x)
all_data_y = np.array(all_data_y)

n_train = 36000
X_train = all_data_x[:n_train]
y_train = all_data_y[:n_train]
X_test = all_data_x[n_train:]
y_test = all_data_y[n_train:]
idx = np.arange(n_train)
np.random.seed(13)
np.random.shuffle(idx)
X_train = X_train[idx]
y_train = y_train[idx]

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

estimators = []
estimators.append(('standardize', StandardScaler()))
estimators.append(('mlp', RandomForestRegressor(n_estimators=200, n_jobs=-1, 
                                     min_samples_split=50, min_samples_leaf=10)))
pipeline = Pipeline(estimators)


pipeline.fit(X_train, y_train)
y_test_est = pipeline.predict(X_test)
print("random forest score: %f" % pipeline.score(X_test, y_test))
print("random forest MSE; %f" % mean_squared_error(y_test, y_test_est))

estimators = []
estimators.append(('standardize', StandardScaler()))
estimators.append(('mlp', Ridge(alpha=1, fit_intercept=True)))
pipeline = Pipeline(estimators)

pipeline.fit(X_train, y_train)
y_test_est = pipeline.predict(X_test)
print("ridge score: %f" % pipeline.score(X_test, y_test))
print("ridge MSE; %f" % mean_squared_error(y_test, y_test_est))


# regression models
avg_pts = X_test[:,8] / X_test[:,1]
print("baseline score: %f" % r2_score(avg_pts, y_test))
print("baseline MSE: %f" % mean_squared_error(avg_pts, y_test))

std = X_train.std(axis=0)
mean = X_train.mean(axis=0)
X_train = (X_train - mean) / std
X_test = (X_test - mean) / std

#===============================================================================
# std = y_train.std(axis=0)
# mean = y_train.mean(axis=0)
# y_train = (y_train - mean) / std
# y_test = (y_test - mean) / std
#===============================================================================

linear_estimator = LinearRegression(fit_intercept=True)
linear_estimator.fit(X_train, y_train)
y_test_est = linear_estimator.predict(X_test)
print("linear regression score: %f" % linear_estimator.score(X_test, y_test))
print("linear regression MSE: %f" % mean_squared_error(y_test, y_test_est))

ridge_estimator = Ridge(alpha=1, fit_intercept=True)
ridge_estimator.fit(X_train, y_train)
y_test_est = ridge_estimator.predict(X_test)
print("ridge regression score: %f" % ridge_estimator.score(X_test, y_test))
print("ridge regression MSE: %f" % mean_squared_error(y_test, y_test_est))

lasso_estimator = Lasso(alpha=0.1, fit_intercept=True)
lasso_estimator.fit(X_train, y_train)
y_test_est = lasso_estimator.predict(X_test)
print("lasso regression score: %f" % lasso_estimator.score(X_test, y_test))
print("lasso regression MSE: %f" % mean_squared_error(y_test, y_test_est))