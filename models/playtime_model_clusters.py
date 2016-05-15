import sys
import numpy as np
from pymongo import MongoClient
from sklearn import linear_model, preprocessing

assert str(sys.argv[1]) is not None
client = MongoClient(str(sys.argv[1]))
db = client.nba_py

allData = []

variables = ['0', '1', '2', '3', '4', 
             '5', '6', '7', '8', '9', 
             '10', '11', '12', '13', '14', 
             '15', '16', '17', '18', '19', ]

cursor = db.playtime_model.find({"PLAYER_GROUP": 1})

count = 0
for document in cursor:
    dataRow = []
    for variable in variables:
        dataRow.append(document[variable])
    dataRow.append(document['MIN'])
    allData.append(dataRow)
    count = count + 1
print("game count: %d" % count)
Xy = np.array(allData)
np.random.shuffle(Xy)
X = Xy[ :, range(0, Xy.shape[1]-1) ]
y = Xy[ :, Xy.shape[1]-1 ]
#--------------------------------------------------------------------- print(Xy)
#---------------------------------------------------------------------- print(X)
#---------------------------------------------------------------------- print(y)
X_normalized = (X)

# Separate into Train and Test datasets
train_test_split = int(round(len(y) * 0.7))
X_normalized_train = X_normalized[:train_test_split]
X_normalized_test = X_normalized[train_test_split:]
y_train = y[:train_test_split]
y_test = y[train_test_split:]

# train model
regr = linear_model.LinearRegression(fit_intercept=True)
regr.fit(X_normalized_train, y_train)

# Coefficients
print('Intercept: ', regr.intercept_)
for i in range(regr.coef_.size):
    print (variables[i], regr.coef_[i])
print("================")
# Error Analysis
print("Residual sum of squares for training set: %.2f"
      % np.mean((regr.predict(X_normalized_train) - y_train) ** 2))
print('Variance score: %.2f' % regr.score(X_normalized_train, y_train))
print("Residual sum of squares for test set: %.2f"
      % np.mean((regr.predict(X_normalized_test) - y_test) ** 2))
print('Variance score: %.2f' % regr.score(X_normalized_test, y_test))

#~~~~calculate against baseline~~~~~~~~~~~
allData = []

cursor = db.playtime_model.find()
for document in cursor:
    dataRow = []
    dataRow.append(document['AVG_MIN'])
    dataRow.append(document['MIN'])
    allData.append(dataRow)
    count = count + 1

Xy = np.array(allData)
np.random.shuffle(Xy)
X = Xy[ :, range(0, Xy.shape[1]-1) ]
y = Xy[ :, Xy.shape[1]-1 ]

X_normalized = (X)

# Separate into Train and Test datasets
train_test_split = int(round(len(y) * 0.7))
X_normalized_train = X_normalized[:train_test_split]
X_normalized_test = X_normalized[train_test_split:]
y_train = y[:train_test_split]
y_test = y[train_test_split:]

regr = linear_model.LinearRegression(fit_intercept=True)
regr.fit(X_normalized_train, y_train)

# Error Analysis
print("Residual sum of squares for Dumb training set: %.2f"
      % np.mean((regr.predict(X_normalized_train) - y_train) ** 2))
print('Variance score: %.2f' % regr.score(X_normalized_train, y_train))
print("Residual sum of squares for Dumb test set: %.2f"
      % np.mean((regr.predict(X_normalized_test) - y_test) ** 2))
print('Variance score: %.2f' % regr.score(X_normalized_test, y_test))

