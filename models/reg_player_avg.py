import sys
import datetime
import time
import numpy as np
from pymongo import MongoClient
from sklearn import linear_model, preprocessing, metrics


assert str(sys.argv[1]) is not None
client = MongoClient(str(sys.argv[1]))
db = client.nba_py

cursor = db.model.find()

allData = []
allDataX = []
allDataY = []

variables = [
    'AVG_PTS',
    'AVG_PTS_LAST_5',
    'AVG_PTS_LAST_1', 
    'PTS'
]


count = 0
for document in cursor:
    if document['MIN'] >= 10:  # 10 minutes or more, to filter outliers
        dataRow = []
        for variable in variables:
            dataRow.append(document[variable])
        allData.append(dataRow)
        allDataX.append(dataRow)
        allDataY.append(document['PTS'])
        count = count + 1
        if count > 20000:
            break
Xy = np.array(allData)
np.random.shuffle(Xy)
X = Xy[:, [0,1,2] ]
y = Xy[:, 3]
print(np.array(allDataX))
print(np.array(allDataY))
print(Xy)
print(X)
print(y)
X_normalized_no_ones = preprocessing.scale(X)


X_normalized = np.ones((X_normalized_no_ones.shape[0], X_normalized_no_ones.shape[1]+1))
X_normalized[:, 1:] = X_normalized_no_ones

print("==================")
print(X_normalized)
# Separate into Train and Test datasets
train_test_split = int(round(len(y) * 0.6))
X_normalized_train = X_normalized[:train_test_split]
X_normalized_test = X_normalized[train_test_split:]
y_train = y[:train_test_split]
y_test = y[train_test_split:]

# train model
regr = linear_model.LinearRegression()
regr.fit(X_normalized_train, y_train)

# The coefficients
print('Coefficients: \n', regr.coef_)
for i in range(regr.coef_.size-1):
    print (variables[i], regr.coef_[i+1])

# The mean square error
print("Residual sum of squares for training set: %.2f"
      % np.mean((regr.predict(X_normalized_train) - y_train) ** 2))
print("Residual sum of squares for test set: %.2f"
      % np.mean((regr.predict(X_normalized_test) - y_test) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regr.score(X_normalized_test, y_test))
# R2 score
print('R2 score: %.2f' % metrics.r2_score(y_test,
                                          regr.predict(X_normalized_test)))

# compare against dumb model which is just the ppg average
print('dumb average RSS: %.2f' % np.mean((X[:, 0] - y) ** 2))
dumb_regr = linear_model.LinearRegression()
X_reshaped = X[:, 0].reshape(-1, 1)
print(X_reshaped.shape)
dumb_regr.fit(X_reshaped, y)
print('dumb average Variance score: %.2f' % dumb_regr.score(X_reshaped, y))
